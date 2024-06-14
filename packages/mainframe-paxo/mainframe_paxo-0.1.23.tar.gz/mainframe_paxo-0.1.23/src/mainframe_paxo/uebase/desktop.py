from __future__ import annotations

import contextlib
import functools
import glob
import json
import os
import os.path
import queue
import re
import shlex
import subprocess
import threading
import time
import uuid
import weakref
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Generator, Iterable, List, Optional, Self, Tuple

import click

from . import config_cache, paths
from . import desktop_win as platform

PLATFORM_WINDOWS = True

# stuff which helps with the engine management on the desktop. Based on the
# DesktopPlatformBase class from the UnrealEngine.


def normalize_root(path: str) -> str:
    return os.path.normcase(os.path.normpath(path))


def is_guid(s: str) -> bool:
    """Check if the string is a guid"""
    try:
        uuid.UUID(hex=s)
        return True
    except ValueError:
        return False


def get_engine_descriptions() -> Iterable[Tuple[str, str, str]]:
    """Get the descriptions of the engines installed on the system."""
    for engine_id, root_dir in platform.enumerate_engine_installations().items():
        yield (engine_id, root_dir, get_engine_description(engine_id, root_dir))


def get_real_path(path):
    name = "%s[%s]" % (path[:-1], path[-1])
    found = glob.glob(name)
    if found:
        return found[0]
    return path


def get_engine_description(identifier: str, root_dir=None, format=False) -> str:
    """Get the description of the engine from the identifier."""
    if is_stock_engine_release(identifier):
        if format:
            return click.style(identifier, fg="green")
        return identifier

    # Otherwise get the path
    root_dir = root_dir or get_engine_root_dir_from_identifier(identifier)
    if not root_dir:
        return ""

    platform_root_dir = os.path.normpath(root_dir)

    # source build
    if is_source_distribution(root_dir):
        prefix = "Source"
    else:
        prefix = "Binary"
    if format:
        return f"{click.style(prefix, fg='cyan')} build at {click.style(platform_root_dir, fg='green')} "
    else:
        return f"{prefix} build at {platform_root_dir}"


def is_stock_engine_release(identifier: str) -> bool:
    """Check if the identifier is a stock engine release."""
    try:
        uuid.UUID(identifier)
        return False
    except ValueError:
        pass

    # classic UE uses only uuids for non-stock engines.  But we allow for
    # other engines, so only if this is a x.y version number do we consider it stock
    match = re.match(r"(\d+\.\d+)", identifier)
    return bool(match)


def get_engine_root_dir_from_identifier(engine_id: str) -> Optional[str]:
    """Look up the engine path from the registry"""
    engines = platform.enumerate_engine_installations()
    return engines.get(engine_id, None)


def get_engine_identifier_from_root_dir(root_dir: str) -> Optional[str]:
    root_dir = normalize_root(root_dir)
    engines = platform.enumerate_engine_installations()

    # we prefer GUID keys to custom keys.
    found = None
    for k, v in engines.items():
        if normalize_root(v) == root_dir:
            if is_guid(k):
                return k
            if not found:
                found = k
    if found:
        return found

    # otherwise, just add it
    return platform.register_engine_installation(root_dir)


def is_valid_root_directory(engine_root):
    """See if this is a proper engine root"""

    # 1 there needs to be an Engine/Binaries folder
    if not os.path.isdir(os.path.join(engine_root, "Engine", "Binaries")):
        return False
    # 2 Also check there's an Engine\Build directory.
    # This will filter out anything that has an engine-like directory structure
    # but doesn't allow building code projects - like the launcher.
    if not os.path.isdir(os.path.join(engine_root, "Engine", "Build")):
        return False

    # 3 Check for a Build.version file.  This will rule out empty directory structures
    if not os.path.isfile(
        os.path.join(engine_root, "Engine", "Build", "Build.version")
    ):
        return False

    # else, we are ok
    return True


def is_source_distribution(engine_root):
    """Check if this is a source distribution"""
    filename = os.path.join(engine_root, "Engine", "Build", "SourceDistribution.txt")
    return os.path.isfile(filename)


def is_perforce_build(engine_root):
    """Check if this is a perforce build"""
    filename = os.path.join(engine_root, "Engine", "Build", "PerforceBuild.txt")
    return os.path.isfile(filename)


def is_preferred_identifier(identifier, other_identifier):
    """Used to sort identifiers for preference"""
    m = re.match(r"(\d+\.\d+)", identifier)
    version = float(m.group(1)) if m else 0.0
    m = re.match(r"(\d+\.\d+)", other_identifier)
    other_version = float(m.group(1)) if m else 0.0
    if version != other_version:
        return version > other_version
    return identifier > other_identifier


def sort_identifiers(identifiers):
    """Sort the identifiers in a preferred order"""
    return sorted(identifiers, key=functools.cmp_to_key(is_preferred_identifier))


class ProjectDirectory:
    cache: Dict[str, ProjectDirectory] = {}

    def __init__(self, root):
        self.root = root
        # project dictionary for a given engine
        roots, projects = self.get_project_dictionary(root)
        self.project_root_dirs = roots
        self.projects = projects

    @classmethod
    def get_project_dictionary(cls, engine_root):
        roots = []
        engine_root = os.path.abspath(engine_root)
        for file in glob.glob(os.path.join(engine_root, "*.uprojectdirs")):
            with open(file) as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith(";"):
                        continue

                    # convert to absolute path
                    if not os.path.isabs(line):
                        line = os.path.join(engine_root, line)
                    line = os.path.normcase(os.path.abspath(line))

                    # is it under the root
                    if line.startswith(os.path.normcase(engine_root)):
                        roots.append(line)
                    else:
                        print(
                            f"Warning: project search path {line} is not under engine root"
                        )

        # Search for all the projects under each root directory
        projects = []
        for root in roots:
            uprojects = glob.glob(os.path.join(root, "*", "*.uproject"))
            for up in uprojects:
                projects.append(
                    (os.path.basename(up), os.path.normcase(os.path.abspath(up)))
                )
        return roots, projects

    @classmethod
    def get(cls, engine_root):
        engine_root = os.path.abspath(engine_root)
        if engine_root in cls.cache:
            return cls.cache[engine_root]

        # create a new one
        result = cls(engine_root)
        cls.cache[engine_root] = result
        return result

    def is_foreign_project(self, project_file_name):
        # a foreign project is one which is not 'native', i.e. outside the engine root
        # check if this project is within the engine
        project_file_name = os.path.normcase(os.path.abspath(project_file_name))
        projects = [x[1] for x in self.projects]
        if project_file_name in projects:
            return False
        # could be a new project, check if its parent dir is in the project root dirs
        project_root_dir = os.path.dirname(project_file_name)
        if project_root_dir in self.project_root_dirs:
            return False

        # ok, must be foreign, then
        return True


# uproject related stuff


def get_engine_identifier_for_project(uproject):
    engine_id = get_engine_association(uproject)

    if is_guid(engine_id):
        return engine_id

    # If identifier doesn't look like a guid, consider it a relative path to test
    # against current dir, and all parent dirs.
    # Absolute paths are also allowed and checked only once
    # Note, this is different behaviour from unreal's standard UnrealVersionSelector:
    # 1. UVS only considers absolute paths, or an empty identifier (meaning
    #    that it searches each parent folder).
    # 2. Standard unreal can not have an engine root in the same folder as the .uproject,
    #    it has to be at least one directory up.  With custom modifications to the engine
    #    it is possible to have the engine root in the same folder as the .uproject.  Various
    #    code in the build system assumes that no engine code can live under the same folder
    #    as the .uproject, so this is a bit of a hack.
    folder = os.path.dirname(uproject)
    lastfolder = ""
    while folder and folder != lastfolder:
        is_abs = os.path.isabs(engine_id) if engine_id else False
        if engine_id and not is_abs:
            check = os.path.join(folder, engine_id)
        else:
            check = folder
        if is_valid_root_directory(check):
            id = get_engine_identifier_from_root_dir(check)
            # remove any trailing slashes from the id, which might have been added
            # to indicate that it was a relative path
            return id.rstrip("\\/")
        if is_abs:
            break
        lastfolder = folder
        folder = os.path.dirname(folder)

    return engine_id.rstrip("\\/")


def set_engine_identifier_for_project(uproject, engine_identifier):
    # read the .uproject file
    assert engine_identifier
    info = read_uproject(uproject)
    if "EngineAssociation" in info:
        info["EngineAssociation"] = engine_identifier
    else:
        # recreate the dict, putting EngineAssociation at position 1 (after FileVersion)
        newinfo = {}
        for i, (key, value) in enumerate(info.items()):
            newinfo[key] = value
            if i == 0:
                newinfo["EngineAssociation"] = engine_identifier
        info = newinfo
    try:
        write_uproject(uproject, info)
        return True
    except OSError:
        return False


def get_engine_association(uproject):
    # read the .uproject file
    info = read_uproject(uproject)
    engine = info.get("EngineAssociation", None)
    return engine


def read_uproject(uproject):
    # read the .uproject file
    with open(uproject) as f:
        info = json.load(f)
    return info


def write_uproject(uproject, info):
    # write the .uproject file
    with open(uproject, "w") as f:
        json.dump(info, f, indent="\t")


@dataclass
class ProjectStatus:
    Name: str
    description: str
    category: str
    code_based_project: bool
    signed_sample_project: bool
    # requires_update: bool
    target_platforms: List[str]


def query_status_for_project(uproject: str) -> ProjectStatus:
    # read the .uproject file
    info = read_uproject(uproject)
    return ProjectStatus(
        Name=info.get("Name", ""),
        description=info.get("Description", ""),
        category=info.get("Category", ""),
        code_based_project=len(info.get("Modules", [])) > 0,
        signed_sample_project=info.get("IsSigned", False),
        # requires_update=info["FileVersion"] < EProjectDescriptorVersion.Latest,
        target_platforms=info.get("TargetPlatforms", []),
    )


def generate_project_files(
    root_dir: str, uproject: str, context: FeedbackContext, logfilepath: str
) -> bool:
    # Generate project files for the given project file

    project_dir = os.path.dirname(uproject)
    paths.set_engine_root(root_dir)
    paths.set_project_root(project_dir)

    args = ["-projectfiles"]

    # Build the arguments to pass to UBT. If it's a non-foreign project, just build full project files.

    # Figure out whether it's a foreign project
    pdir = ProjectDirectory.get(root_dir)
    if uproject and pdir.is_foreign_project(uproject):
        args.append(f"-project={os.path.abspath(uproject)}")

        # always include game source
        args.append("-game")

        # determine whether or not to include engine source
        if is_source_distribution(root_dir):
            args.append("-engine")
        else:
            # if this is used within UnrealVersionSelector then we still need to pass
            # -rocket to deal with old versions that don't use Rocket.txt file
            args.append("-rocket")

    args.append("-progress")

    if logfilepath:
        args.append(f"-log={logfilepath}")

    # Compile UnrealBuildTool if it doesn't exist. This can happen if we're just copying source from somewhere.

    success = True
    with context.slow("Generating project files...") as slow:
        if not os.path.exists(get_unreal_build_tool_executable_filename(root_dir)):
            slow.progress_message("Building UnrealBuildTool...")
            success = build_unreal_build_tool(root_dir, slow)
        if success:
            msg = "Generating project files..."
            slow.progress_message(msg)
            success = run_unreal_build_tool(msg, root_dir, args, slow)
        return success


def get_unreal_build_tool_executable_filename(root_dir: str) -> str:
    """Get the filename of the UnrealBuildTool executable"""
    # First, try loading it from the config file:
    configpath = os.path.join(root_dir, "Engine", "Config")
    config = config_cache.load_external_ini_file(
        ini_name="Engine",
        engine_config_dir=configpath,
        source_config_dir=configpath,
        is_base_ini_name=True,
        platform="",
        force_reload=False,
        write_dest_ini=False,
    )
    if config:
        entry = config.get("PlatformPaths", "UnrealBuildTool", fallback=None)
        if entry:
            return os.path.abspath(os.path.join(root_dir, entry))

    # use default
    return os.path.abspath(
        os.path.join(
            root_dir, "Engine/Binaries/DotNET/UnrealBuildTool/UnrealBuildTool.exe"
        )
    )


def get_unreal_build_tool_project_filename(root_dir):
    path = "Engine/Source/Programs/UnrealBuildTool/UnrealBuildTool.csproj"
    return os.path.abspath(os.path.join(root_dir, path))


def build_unreal_build_tool(root_dir, warn):
    warn.log(f"Building UnrealBuildTool in {root_dir}...")

    cs_proj_location = get_unreal_build_tool_project_filename(root_dir)
    if not os.path.isfile(cs_proj_location):
        warn.log(f"Project file not found at {cs_proj_location}")
        # return False

    if PLATFORM_WINDOWS:
        compiler_exe_filename = platform.try_read_msbuild_install_path()
        if not compiler_exe_filename:
            warn.log("Couldn't find MSBuild installation; skipping.")
            # return False
            compiler_exe_filename = "wonko.exe  "

        cmdline_params = [
            "/nologo",
            "/verbosity:quiet",
            cs_proj_location,
            "/property:Configuration=Development",
            "/property:Platform=AnyCPU",
        ]
    else:
        warn.log("Unknown platform, unable to build UnrealBuildTool.")
        return False

    warn.log(f"Running: {compiler_exe_filename} {cmdline_params}")
    success, code = warn.run_process(
        "Building UnrealBuildTool", [compiler_exe_filename] + cmdline_params
    )
    if not success or code != 0:
        return False

    # If the executable appeared where we expect it, then we were successful
    exe_path = get_unreal_build_tool_executable_filename(root_dir)
    if not os.path.isfile(exe_path):
        warn.log(f"Missing {exe_path} after build")
        return False
    return True


def run_unreal_build_tool(msg, root_dir, args, warn):
    return platform.run_unreal_build_tool(msg, root_dir, args, warn)


class FeedbackSink(ABC):
    """An object which receives feedback events"""

    @abstractmethod
    def log(self, message: str, level: str = "info") -> None:
        """Log a message to the user"""

    @abstractmethod
    def progress_message(self, message: str) -> None:
        """Report progress message to the user"""

    @abstractmethod
    def progress_value(self, value: float) -> None:
        """Report progress fraction to the user"""

    @abstractmethod
    def poll(self, delay: float = 0.0) -> str:
        """Poll the user interaction.  Can be used to perform window updates
        or to check for user interaction.  Returns a string which can be used
        to perform operations, such as "cancel" or "pause".
        """


class FeedbackContext(FeedbackSink):
    """
    A feedback context is a context which can be used to provide feedback to the user
    typically via the interactive console or with a window.
    """

    def __init__(self, parent: FeedbackContext | None = None) -> None:
        if parent is None:
            self.root = weakref.proxy(self)
        else:
            self.root = parent.root
        self.parent = parent
        self.log_lines: list[tuple[str, str]] = []
        self.current_slow_task: str | None = None

    def log(self, message, level: str = "INFO") -> None:
        """Log a message to the user"""
        if self.parent:
            self.root.log(message, level)
            return
        self.log_lines.append((level, message))

    def get_logs(self, show_level: bool = False) -> str:
        if show_level:
            return "".join(f"{level}: {message}\n" for level, message in self.log_lines)
        else:
            return "".join(f"{message}\n" for level, message in self.log_lines)

    def begin_slow_task(self, message: str, **kwargs) -> None:
        assert self.current_slow_task is None
        self.current_slow_task = message
        self.progress_message(message)

    def end_slow_task(self) -> None:
        assert self.current_slow_task is not None
        self.current_slow_task = None

    @contextlib.contextmanager
    def slow(self, message: str, nested=True, **kwargs) -> Generator[Self, None, None]:
        """A context manager for slow tasks"""
        if nested:
            ctx = self.__class__(parent=self)
        else:
            ctx = self
        ctx.begin_slow_task(message, **kwargs)
        try:
            yield ctx
        finally:
            ctx.end_slow_task()

    def poll(self, delay: float = 0.0) -> str:
        """Poll the user interaction.  Can be used to perform window updates
        or to check for user interaction.  Returns a string which can be used
        to perform operations, such as "cancel" or "pause".
        """
        if delay:
            time.sleep(delay)
        return ""

    def run_process(self, message, args, **kwargs) -> Tuple[bool, int]:
        with self.slow(message) as slow:
            try:
                p = subprocess.Popen(
                    args,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    creationflags=subprocess.CREATE_NO_WINDOW,
                    **kwargs,
                )
            except OSError as e:
                slow.log(f"Could not create process {args}: {e}", level="error")
                return (False, -1)

            # now read the pipe and output each line to the slow context
            # until we don't get any more lines
            assert p.stdout is not None
            reader = NBReader(p.stdout)
            while True:
                line = reader.try_readline()
                if line == "":
                    break  # end of file
                if line is None:
                    # no data, work the io context for a bit
                    poll = self.poll(0.1)
                    if poll == "cancel":
                        p.terminate()
                        break
                    continue
                line = line.rstrip()
                if self.parse_command(line):
                    continue
                slow.log(line)

            p.wait()
            if p.returncode:
                slow.log(f"Process {args} exited with code {p.returncode}")
            return (True, p.returncode)

    def parse_command(self, line: str) -> bool:
        # search for a message of the form
        # "@progress ["msg"|'msg'] nominator denominator"
        if not line.startswith("@progress"):
            return False
        try:
            parts = shlex.split(line)
        except ValueError:
            return False
        if parts and parts[0] == "@progress":
            del parts[0]
            msg = None
            while len(parts):
                try:
                    if parts[0].endswith("%"):
                        fraction = float(parts[0][:-1]) / 100
                    elif len(parts) >= 2:
                        nominator = int(parts[0])
                        denominator = int(parts[1])
                        fraction = nominator / denominator if denominator else 0
                    self.progress_value(fraction)
                    break
                except ValueError:
                    msg = parts[0]
                    del parts[0]
            if msg:
                self.progress_message(msg)
                return True
        return False


class NBReader:
    def __init__(self, stream):
        self.stream = stream
        self.queue = queue.SimpleQueue()
        self.thread = threading.Thread(target=self.enqueue)
        self.stop = False
        self.thread.start()

    def enqueue(self):
        # read the pipe and output each line to the slow context until an
        # empty line is received, signalling the end of the process
        try:
            while not self.stop:
                line = self.stream.readline()
                if not line:
                    break
                self.queue.put(line)
        finally:
            self.queue.put("")

    def try_readline(self, timeout: float = 0.0) -> str | None:
        try:
            if timeout:
                return self.queue.get(timeout=timeout)
            return self.queue.get(block=False)
        except queue.Empty:
            return None


class ClickFeedbackContext(FeedbackContext):
    """A progress context which uses click to display progress"""

    def __init__(self, parent=None, click_ctx=None):
        super().__init__(parent=parent)
        self.click_ctx = click_ctx
        if not click_ctx and self.parent:
            self.click_ctx = self.parent.click_ctx
        self.last_msg = None

    @contextlib.contextmanager
    def slow(self, msg, *args, **kwargs):
        with click.progressbar(
            length=100, label=msg, show_eta=False, show_percent=True
        ) as bar:
            yield self.__class__(parent=self, click_ctx=bar)

    def progress_message(self, message: str) -> None:
        assert self.click_ctx is not None
        if message != self.last_msg:
            click.echo(message)
            self.last_msg = message

    def progress_value(self, fraction: float) -> None:
        self.click_ctx.update(int(fraction * 100))

    def log(self, message, level="info"):
        super().log(message, level)
        level = level.lower()
        if "error" in level:
            click.secho(message, fg="red")
        elif "warn" in level:
            click.secho(message, fg="yellow")
        else:
            click.echo(message)


class SinkFeedbackContext(FeedbackContext):
    def __init__(
        self,
        parent: SinkFeedbackContext | None = None,
        sink: FeedbackSink | None = None,
    ):
        super().__init__(parent=parent)
        self.sink: FeedbackSink
        if parent is None:
            assert sink is not None
            self.sink = sink
        else:
            self.sink = parent.sink

    def progress_message(self, message: str) -> None:
        self.sink.progress_message(message)

    def progress_value(self, value: float) -> None:
        return self.sink.progress_value(value)

    def log(self, message, level: str = "INFO") -> None:
        super().log(message, level)
        self.sink.log(message, level)

    def poll(self, delay: float = 0.0) -> str:
        return self.sink.poll(delay)
