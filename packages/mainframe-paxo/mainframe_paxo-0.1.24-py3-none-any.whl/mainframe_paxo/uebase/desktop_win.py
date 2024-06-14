import ctypes
import ctypes.wintypes
import os.path
import shlex
import uuid
from typing import Dict, Optional

import click

from ..registry import Key
from . import desktop


def enumerate_engine_installations() -> Dict[str, str]:
    launcher_engines = enumerate_launcher_engine_installations()
    user_engines = enumerate_user_engine_installations()
    launcher_engines.update(user_engines)
    return launcher_engines


def enumerate_launcher_engine_installations() -> Dict[str, str]:
    """Enumerate the engine installations from the launcher"""

    result: Dict[str, str] = {}
    with Key.local_machine(
        "SOFTWARE\\EpicGames\\Unreal Engine",
        check=False,
    ) as key:
        if not key:
            return result
        for subkey in key.subkeys():
            with subkey:
                name = subkey.name
                root = subkey.get("InstalledDirectory", None)
                if root and desktop.is_valid_root_directory(root):
                    result[name] = desktop.normalize_root(root)
    return result


def enumerate_user_engine_installations() -> Dict[str, str]:
    """Enumerate the engine installations from the launcher"""

    result: Dict[str, str] = {}
    remove = []  # values to remove
    unique_directories = set()

    with Key.current_user(
        "SOFTWARE\\Epic Games\\Unreal Engine\\Builds", write=True
    ) as key:
        if not key:
            return result
        for k, v in key.items():
            n = desktop.normalize_root(v)
            ok = False
            if desktop.is_valid_root_directory(v):
                try:
                    guid = uuid.UUID(k)
                except ValueError:
                    guid = None
                if guid:
                    # clean out duplicate guid keys for the same engine
                    if n not in unique_directories:
                        unique_directories.add(n)
                        ok = True
                else:
                    # we accept all non-guid keys, since they were created by the user
                    ok = True
            if ok:
                result[k] = v
            else:
                remove.append(k)

        # Remove all the keys which weren't valid
        for k in remove:
            del key[k]
    return result


def register_engine_installation(
    root_dir: str, engine_id: Optional[str] = None
) -> Optional[str]:
    """Register an engine installation"""
    if not desktop.is_valid_root_directory(root_dir):
        return None
    if not engine_id:
        engine_id = str(uuid.uuid4())
    return register_engine_installation_identifier(root_dir, engine_id)


def register_engine_installation_identifier(root_dir: str, engine_id: str) -> str:
    with Key.current_user(
        "SOFTWARE\\Epic Games\\Unreal Engine\\Builds", create=True
    ) as key:
        if desktop.is_guid(engine_id):
            root_dir = desktop.normalize_root(root_dir)
            # check if there is a guid key with the same root dir
            for k, v in key.items():
                if desktop.is_guid(k) and desktop.normalize_root(v) == root_dir:
                    # we just re-use the existing guid key
                    return k
        key[engine_id] = root_dir
    return engine_id


def update_file_associations(
    engine_root=None, handler=None, user=True, verify=True, test=False
):
    # the engine contains a special execution to act as a shell handler
    # for files with the .uproject extension

    if not handler:
        handler = os.path.join(
            engine_root, "Engine", "Binaries", "Win64", "UnrealVersionSelector.exe"
        )
        handler = [os.path.abspath(handler)]
    elif not isinstance(handler, list):
        handler = [handler]
    handler[0] = os.path.abspath(handler[0])

    # we need to find an icon for the handler
    paxoicon = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "paxo.ico")
    )
    iconhandler = handler[0]
    if not os.path.exists(handler[0]):
        iconhandler = paxoicon
    # or, if it is not UnrealVersionSelector, use the icon from paxo
    if "UnrealVersion" not in os.path.basename(handler[0]):
        iconhandler = paxoicon

    # quoted handler for the registry
    quoted_handler = " ".join(f'"{f}"' for f in handler)
    quoted_iconhandler = f'"{iconhandler}"'
    quoted_paxoicon = f'"{paxoicon}"'
    set_associations(user, quoted_handler, quoted_iconhandler, quoted_paxoicon)


def set_associations(user: bool, handler: str, fileicon: str, cmdicon: str):
    # we must now find the appropriate place in the registry and add it.abs
    # this is a bit tricky, but we can use the python winreg module
    if user:
        root = Key.current_user("Software\\Classes")
    else:
        root = Key.local_machine("Software\\Classes")
    with root.create(".uproject") as key:
        key[""] = "Unreal.ProjectFile"

    with root.create("Unreal.ProjectFile") as key:
        # we could well clear this subtree first and write it all fresh
        key[""] = "Unreal Engine Project File"
        key["VersionSelectorExecutable"] = handler

        # the DefaultIcon subkey, used for the shell in the file
        with key.create("DefaultIcon") as subkey:
            subkey[""] = fileicon

        with key.create("shell") as subkey:

            def add(name, description, command):
                with subkey.create(name) as k2:
                    k2[""] = description
                    with k2.create("command") as k3:
                        k3[""] = command
                    with k2.create("icon") as k3:
                        k3[""] = cmdicon

            add("open", "Open", handler + ' /editor "%1"')
            add("run", "Launch game", handler + ' /game "%1"')
            add(
                "rungenproj",
                "Generate Visual Studio project files",
                handler + ' /projectfiles "%1"',
            )
            add(
                "switchversion",
                "Switch Unreal Engine version...",
                handler + ' /switchversion "%1"',
            )
            add("hotdog", "Get some sausages...", "explorer.exe https://hot-dog.org")

    clear_custom_shell_association()
    return handler


def clear_custom_shell_association():
    # If the user has manually selected something other than our extension,
    # we need to delete it.
    # Explorer explicitly disables set access on that keys
    # in that folder, but we can delete the whole thing.
    user_choice = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\FileExts\\.uproject\\UserChoice"
    key = Key.current_user(user_choice)
    if key:
        key.delete(tree=True)


def verify_file_associations(user=True, silent=False):
    clear_custom_shell_association()
    try:
        if user:
            root = Key.current_user("Software\\Classes")
        else:
            root = Key.local_machine("Software\\Classes")

        with root(".uproject", check=False) as key:
            if not key or key[""] != "Unreal.ProjectFile":
                raise click.ClickException(
                    f"File association for .uproject not set for scope {'user' if user else 'machine'}"
                )
        with root("Unreal.ProjectFile", check=False) as key:
            if not key:
                raise click.ClickException(
                    f"File association for Unreal.ProjectFile not set for scope {'user' if user else 'machine'}"
                )

            with key("shell", "open", "command", check=False) as key:
                if not key:
                    raise click.ClickException(
                        f"Unreal.ProjectFile shell not set for scope {'user' if user else 'machine'}"
                    )

                try:
                    handler = key[""]
                except KeyError:
                    handler = ""
                if not handler:
                    raise click.ClickException(
                        f"Unreal.ProjectFile shell open command not set for scope {'user' if user else 'machine'}"
                    )
                parts = shlex.split(handler)
                try:
                    editor_index = parts.index("/editor")
                except ValueError:
                    raise click.ClickException(
                        f"Unreal.ProjectFile shell open command does not contain /editor for scope {'user' if user else 'machine'}"
                    )
                return True, parts[:editor_index]
    except click.ClickException as e:
        if silent:
            return False, e.format_message()
        raise


def get_file_associations_handler(user: bool = True) -> list[str] | None:
    if user:
        root = Key.current_user("Software\\Classes")
    else:
        root = Key.local_machine("Software\\Classes")
    try:
        with root(".uproject") as key:
            if key[""] != "Unreal.ProjectFile":
                return None
        with root("Unreal.ProjectFile") as key:
            with key("shell", "open", "command") as key:
                handler = key[""]
                parts = shlex.split(handler)
                try:
                    editor_index = parts.index("/editor")
                    return parts[:editor_index]
                except ValueError:
                    pass
                return parts
    except (KeyError, ValueError):
        return None


def clear_file_associations(user=True):
    if user:
        root = Key.current_user("Software\\Classes")
    else:
        root = Key.local_machine("Software\\Classes")

    key = root(".uproject")
    if key:
        key.delete(tree=True)
    key = root("Unreal.ProjectFile")
    if key:
        key.delete(tree=True)
    clear_custom_shell_association()


def try_read_msbuild_install_path() -> Optional[str]:
    # first try the location in program files
    program_files = get_program_files_folder()
    if program_files:
        tool_path = os.path.join(program_files, "MSBuild/14.0/bin/MSBuild.exe")
        if os.path.exists(tool_path):
            return tool_path

    # Try to get the MSBuild 14.0 path directly (see https://msdn.microsoft.com/en-us/library/hh162058(v=vs.120).aspx)
    path = try_lookup_msbuild_install_path(
        "Microsoft\\MSBuild\\ToolsVersions\\14.0", "MSBuildToolsPath", "MSBuild.exe"
    )

    # Check for MSBuild 15. This is installed alongside Visual Studio 2017, so we get the path relative to that.
    path = path or try_lookup_msbuild_install_path(
        "Microsoft\\VisualStudio\\SxS\\VS7", "15.0", "MSBuild\\15.0\\bin\\MSBuild.exe"
    )

    # Check for older versions of MSBuild. These are registered as separate versions in the registry.
    path = path or try_lookup_msbuild_install_path(
        "Microsoft\\MSBuild\\ToolsVersions\\12.0", "MSBuildToolsPath", "MSBuild.exe"
    )
    path = path or try_lookup_msbuild_install_path(
        "Microsoft\\MSBuild\\ToolsVersions\\4.0", "MSBuildToolsPath", "MSBuild.exe"
    )
    return path


def get_known_folder_path(folder_id: uuid.UUID) -> str:
    dll = ctypes.windll.shell32
    buf = ctypes.c_wchar_p()
    dll.SHGetKnownFolderPath(
        folder_id.bytes_le, ctypes.wintypes.DWORD(), None, ctypes.byref(buf)
    )
    result = buf.value
    ctypes.windll.Ole32.CoTaskMemFree(buf)
    return result or ""


def get_program_files_folder() -> str:
    """Get the program files folder using the proper ShGetKnowFolderPath function.  This is the correct way to do it."""
    FOLDERID_ProgramFiles = uuid.UUID("{905e63b6-c1bf-494e-b29c-65b732d3d21a}")
    return get_known_folder_path(FOLDERID_ProgramFiles)


_user_settings_dir = ""


def user_settings_dir() -> str:
    global _user_settings_dir
    if not _user_settings_dir:
        FOLDERID_LocalAppData = uuid.UUID("{F1B32785-6FBA-4FCF-9D55-7B8E7F157091}")
        _user_settings_dir = get_known_folder_path(FOLDERID_LocalAppData)
    return _user_settings_dir


_user_dir = ""


def user_dir() -> str:
    global _user_dir
    if not _user_dir:
        FOLDERID_Documents = uuid.UUID("{FDD39AD0-238F-46AF-ADB4-6C85480369C7}")
        _user_dir = get_known_folder_path(FOLDERID_Documents)
    return _user_dir


def try_lookup_msbuild_install_path(
    key_relative: str, value_name: str, relative_path: str
) -> Optional[str]:
    def lookup(rootkey: Key, key_name: str) -> Optional[str]:
        with rootkey(key_name, key_relative, check=False) as key:
            if key is not None:
                value = key.get(value_name, None)
                if value:
                    fn = os.path.join(value, relative_path)
                    if os.path.exists(fn):
                        return fn
        return None

    path = lookup(Key.current_user(), "SOFTWARE")
    path = path or lookup(Key.local_machine(), "SOFTWARE")
    path = path or lookup(Key.current_user(), "SOFTWARE\\Wow6432Node")
    path = path or lookup(Key.local_machine(), "SOFTWARE\\Wow6432Node")
    return path


def run_unreal_build_tool(msg, root_dir, args, warn) -> bool:
    # Get the path to UBT
    unreal_build_tool_path = desktop.get_unreal_build_tool_executable_filename(root_dir)
    if not unreal_build_tool_path or not os.path.isfile(unreal_build_tool_path):
        warn.log(
            f"Couldn't find UnrealBuildTool at '{unreal_build_tool_path}'", type="ERROR"
        )
        return False

    warn.log(f"Running {unreal_build_tool_path} {args}")

    success, returncode = warn.run_process(msg, [unreal_build_tool_path] + args)
    return success and returncode == 0
