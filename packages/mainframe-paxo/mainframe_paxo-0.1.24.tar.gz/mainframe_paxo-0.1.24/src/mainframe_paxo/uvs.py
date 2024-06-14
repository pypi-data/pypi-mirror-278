import datetime
import json
import logging
import os.path
import re
import subprocess
import sys
import tkinter as tk
import tkinter.messagebox
from typing import List, Optional

import click

from . import log, tools, ue
from .uebase import desktop
from .uvs_gui import EngineSelector, ProjectFilesWindow

# our custom version of UnrealVersionSelector.exe

logger = logging.getLogger(__name__)
use_gui = sys.executable.endswith("pythonw.exe")


def find_icon():
    # we need to find an icon for the handler
    paxoicon = os.path.abspath(os.path.join(os.path.dirname(__file__), "paxo.ico"))
    if not os.path.isfile(paxoicon):
        return None
    return paxoicon


def abort(msg):
    raise click.ClickException(msg)


@click.group(invoke_without_command=False)
@click.option("--gui/--no-gui", default=use_gui, help="run with or without gui")
@click.option("--verbose", "-v", is_flag=True, help="Enables verbose mode.")
@click.pass_context
def uvs(ctx, gui, verbose):
    """A python version of the UnrealVersionSelector.exe.

    Initial command can be prefixed with a single dash or slash."""
    global use_gui
    use_gui = gui
    if verbose:
        log.init()  # ("DEBUG")

    if ctx.invoked_subcommand is None:
        # if this were part of engine, we could register _this_ engine with prompt
        # but since it's not, we don't support this functionality
        # of invoking UnrealVersionSelector.exe with no arguments.
        pass


cli = uvs


@cli.command()
@click.option("--unattended", is_flag=True, help="Don't prompt for input")
@click.argument("engine_id", default="")
@click.option(
    "--engine-root",
    type=click.Path(exists=True),
    help="The engine root to register",
)
def register(engine_id, unattended, engine_root):
    """Register a _this_ engine.  Not supported."""
    register_current_engine_directory(engine_id, unattended, engine_root)


def register_current_engine_directory(
    engine_id=None, unattended=False, engine_root=None
):
    if not engine_root:
        abort("can't register _this_engine, because this is a standalone tool")
    engine_root = os.path.abspath(engine_root)
    if not desktop.is_valid_root_directory(engine_root):
        abort(f"Invalid engine root {engine_root}")

    if not engine_id:
        engine_id = desktop.get_engine_identifier_from_root_dir(engine_root)
        if not engine_id:
            abort(f"Can't find engine identifier for {engine_root}")

    desktop.platform.register_engine_installation_identifier(engine_root, engine_id)

    # check if file handlers are in place
    if not desktop.platform.get_file_associations_handler(
        user=True
    ) and not desktop.platform.get_file_associations_handler(user=False):
        if unattended:
            do_it = True
        else:
            do_it = messagebox_yesno(
                msg="Register Unreal Engine file types?", heading="File Types"
            )
        if do_it:
            # okay, we update it.  Use uvs as a handler (overrides engine_root if present)
            handler = find_run_args(gui=True)
            desktop.platform.update_file_associations(
                engine_root=engine_root, handler=handler
            )

    click.echo(f"Registered engine {engine_id} at {engine_root}")


# flags are non-standard extensions to the original UnrealVersionSelector.exe
@cli.command()
@click.option("--check", is_flag=True, help="Check file associations.")
@click.option("--clear", is_flag=True, help="Remove associations.")
@click.option("--user", is_flag=True, help="use 'user' scope instead of 'machine'")
@click.option(
    "--engine-root",
    type=click.Path(exists=True),
    help="The engine root for the UnrealVersionSelector.exe to use",
)
def fileassociations(check, clear, user, engine_root):
    """Register file associations"""

    update_file_associations(check, clear, user, engine_root)


def update_file_associations(
    check=False,
    clear=False,
    user=True,
    handler: list[str] | None = None,
    engine_root=None,
):
    if check:
        for user in [True, False]:
            ok, handler = desktop.platform.verify_file_associations(
                user=user, silent=True
            )
            if not ok:
                click.secho(handler, fg="yellow")
            else:
                click.echo(
                    f"File associations for scope {'user' if user else 'machine'}: {handler!r}"
                )
                assert handler is not None
                if not os.path.isfile(handler[0]):
                    click.secho(f"File handler {handler[0]} does not exist.", fg="red")
    elif clear:
        desktop.platform.clear_file_associations(user=user)
        click.echo(
            f"File associations cleared for scope {'user' if user else 'machine'}"
        )
    else:
        if not handler and not engine_root:
            handler = find_run_args(gui=True)
        desktop.platform.update_file_associations(
            handler=handler, engine_root=engine_root, verify=True
        )
        click.echo(
            f"File associations updated for scope {'user' if user else 'machine'}"
        )


# non-standard extension to the original UnrealVersionSelector.exe
@cli.command()
@click.argument(
    "uproject", type=click.Path(exists=True), default=None, metavar="<.uproject>"
)
@click.option(
    "--engine-root",
    type=click.Path(exists=True),
    help="The engine root to return the identifier for",
)
def identifier(uproject, engine_root):
    """Print the identifier for the project"""
    if engine_root:
        identifier = desktop.get_engine_identifier_from_root_dir(engine_root)
    else:
        identifier = desktop.get_engine_identifier_for_project(uproject)
    messagebox_ok(identifier, True, "Engine Identifier")


# non-standard extension to the original UnrealVersionSelector.exe
@cli.command()
@click.argument("uproject", type=click.Path(exists=True), metavar="<.uproject>")
def engineroot(uproject):
    """Print the engine root for the project"""
    root = get_project_engine(uproject)
    messagebox_ok(root, True, "Engine Root")


def get_project_engine(uproject):
    engine_id = desktop.get_engine_identifier_for_project(uproject)
    if not engine_id:
        raise click.ClickException(f"Can't find engine identifier for {uproject}")

    engine_root = desktop.get_engine_root_dir_from_identifier(engine_id)
    if not engine_root:
        raise click.ClickException(f"Can't find engine root for {engine_id}")
    return engine_root


@cli.command()
@click.argument("uproject", type=click.Path(exists=True), metavar="<.uproject>")
@click.option(
    "--engine_id", metavar="<engine_id>", default=None, help="The engine id to use"
)
def switchversion(uproject, engine_id):
    """Switch the engine version for the project"""

    current_engine_id = desktop.get_engine_identifier_for_project(uproject)
    engines = desktop.platform.enumerate_engine_installations()
    if not engine_id:
        engine_id = select_engine_installation(engines, initial_id=current_engine_id)
    elif engine_id not in engines:
        abort(f"Unknown engine id {engine_id}")

    if not engine_id or engine_id == current_engine_id:
        return

    if not desktop.set_engine_identifier_for_project(uproject, engine_id):
        abort(
            f"Failed to set engine id {engine_id} for {uproject}.  Check if the file is writeable."
        )

    # if it is a content only project, we are done
    status = desktop.query_status_for_project(uproject)
    if not status.code_based_project:
        return

    # Need to rebuild project files
    return generate_project_files(uproject)


@cli.command()
@click.argument("uproject", type=click.Path(exists=True), metavar="<.uproject>")
def editor(uproject):
    """Start the editor for project"""
    return launch_editor(uproject)


@cli.command()
@click.argument("uproject", type=click.Path(exists=True), metavar="<.uproject>")
def projectlist(uproject):
    """Start the editor with a list of projects"""
    return launch_editor()


@cli.command()
@click.argument("uproject", type=click.Path(exists=True), metavar="<.uproject>")
def game(uproject):
    """Start the editor for the project and run the game"""
    return launch_editor(uproject, ["-game"])


@cli.command()
@click.argument("uproject", type=click.Path(exists=True), metavar="<.uproject>")
def projectfiles(uproject):
    """Rebuild project files for the project"""
    # editor = ue.get_editor_from_uproject()
    return generate_project_files(uproject)


def launch_editor(uproject: Optional[str] = None, args: List[str] = []):
    """Start the editor for project"""

    if not uproject:
        engines = desktop.platform.enumerate_engine_installations()
        engine_id = select_engine_installation(engines)
        if not engine_id:
            return False
        root_dir = desktop.get_engine_root_dir_from_identifier(engine_id)
        logger.debug("Found engine root %s for id %s", root_dir, engine_id)
        if not platform_launch_editor(root_dir, None, args):
            abort("Failed to launch editor")
        return True

    root = get_validated_engine_root(uproject)
    logger.debug("Found engine root %s for project %s", root, uproject)
    if not root:
        return False
    # Figure out the path to the editor executable. This may be empty for older .target files
    editor_filename = try_get_editor_filename(os.path.join(root, "Engine"), uproject)
    logger.debug("Found editor filename %s", editor_filename)

    if not platform_launch_editor(root, editor_filename, [uproject] + args):
        abort("Failed to launch editor")
    return True


def get_validated_engine_root(uproject: str) -> Optional[str]:
    root = get_engine_root_dir_for_project(uproject)
    if not root:
        if not switchversion(uproject, None):
            return None
    root = get_engine_root_dir_for_project(uproject)
    if not root:
        abort("Error retrieving project root directory")
    return root


def get_engine_root_dir_for_project(uproject: str) -> Optional[str]:
    engine_id = desktop.get_engine_identifier_for_project(uproject)
    if not engine_id:
        return None
    return desktop.get_engine_root_dir_from_identifier(engine_id)


def try_get_editor_filename(engine_engine: str, uproject: str) -> Optional[str]:
    """Try to find the editor filename for the uproject"""
    project_dir = os.path.dirname(uproject)
    binaries_dir = os.path.join(project_dir, "Binaries", "Win64")
    if os.path.isdir(binaries_dir):
        # find all .target files in the binaries directory and sort them by modification time
        target_files = []
        for root, dirs, files in os.walk(binaries_dir):
            del dirs[:]
            for file in files:
                if file.endswith(".target"):
                    f = os.path.join(root, file)
                    target_files.append((f, os.path.getmtime(f)))
        target_files.sort(key=lambda x: x[1], reverse=True)
        # look for launch path in the target files, last modification first.
        for target_file, _ in target_files:
            launch_path = read_launch_path_from_target_file(target_file)
            logger.debug("Found launch path %s in %s", launch_path, target_file)
            if launch_path:
                # replace $(EngineDir) with the engine's Engine directory
                launch_path = re.sub(
                    r"\$\(EngineDir\)",
                    lambda f: engine_engine,
                    launch_path,
                    flags=re.IGNORECASE,
                )
                launch_path = re.sub(
                    r"\$\(ProjectDir\)",
                    lambda f: project_dir,
                    launch_path,
                    flags=re.IGNORECASE,
                )
                return launch_path
    return None


def read_launch_path_from_target_file(target_file: str) -> Optional[str]:
    """Read the launch path from the target file"""
    with open(target_file, "r") as f:
        try:
            info = json.load(f)
        except json.JSONDecodeError:
            return None

    # Check it's an editor target
    if info.get("TargetType") != "Editor":
        return None
    # Check it's development configuration
    if info.get("Configuration") != "Development":
        return None
    return info.get("Launch", None)


def platform_launch_editor(
    root_dir: Optional[str], explicit_filename: Optional[str], args: List[str]
) -> bool:
    """Launch the editor for the project"""
    if not explicit_filename:
        assert root_dir
        filename = explicit_filename or os.path.join(
            root_dir, "Engine", "Binaries", "Win64", "UnrealEditor.exe"
        )
    else:
        filename = explicit_filename

    try:
        logger.info("%s", f"Launching editor: {[filename] + args}")
        subprocess.Popen([filename] + args)
    except OSError:
        return False
    return True


def generate_project_files(uproject):
    # check if it is a code project
    # hm, why not use ProjectDescriptor?
    # project = ProjectDescriptor.load(uproject)
    source_dir = os.path.join(os.path.dirname(uproject), "Source")
    if not os.path.isdir(source_dir):
        abort(
            "This project does not have any source code. You need to add C++ source files to the project from the Editor before you can generate project files."
        )

    root_dir = get_validated_engine_root(uproject)
    if not root_dir:
        return False

    exename = "paxo"
    now = datetime.datetime.now().strftime("%Y.%m.%d-%H.%M.%S")
    logfile = os.path.join(
        os.path.dirname(uproject), "Saved", "Logs", f"{exename}-{now}.log"
    )

    if use_gui:
        window = ProjectFilesWindow()
        context = desktop.SinkFeedbackContext(sink=window)
    else:
        window = None
        context = desktop.ClickFeedbackContext()
    try:
        ok = desktop.generate_project_files(root_dir, uproject, context, logfile)
        if not ok:
            log = context.get_logs()
            messagebox_ok(log, False, "Failed to generate project files.")
            return False
        return True
    finally:
        if window:
            window.close()


# @cli.command()
def register_test():
    """Register uvs as the default UnrealVersionSelector"""
    print(sys.argv)
    print(__spec__)
    print(sys.executable)
    return
    # find the command used to run us
    cmd = sys.argv[:]
    i = cmd.index("register-test")
    cmd = cmd[:i]
    # remove any trailing args
    while cmd[-1].startswith("-"):
        cmd.pop()

    # if we are running a .py file, we need to use the -m flag with the actual
    # module name (not __main__)
    if cmd[0].endswith(".py"):
        exe = sys.executable
        if exe.endswith("python.exe"):
            exe = exe[:-10] + "pythonw.exe"
        cmd = [exe, "-m", __spec__.name] + cmd[1:]

    ue.register_uproject_handler(engine_path=None, handler=cmd, test=True)


def find_run_args(gui: bool = True) -> List[str]:
    """Find the command to run this script using python"""
    exe = sys.executable
    if gui:
        # on windows, find the pythonw.exe if it exists
        base = os.path.basename(exe)
        if os.path.normcase(base) == "python.exe":
            exew = os.path.join(os.path.dirname(exe), "pythonw.exe")
            if os.path.isfile(exew):
                exe = exew
    return [exe, "-m", __spec__.name]  # type: ignore[name-defined]


def messagebox_ok(
    message: str,
    success: bool = True,
    heading: Optional[str] = None,
    parent: Optional[tk.Tk] = None,
) -> bool:
    if not heading:
        heading = "Success" if success else "Error"

    if use_gui:
        if success:
            tkinter.messagebox.showinfo(heading, message, parent=parent)
        else:
            tkinter.messagebox.showerror(heading, message, parent=parent)
    else:
        # just use echo
        if success:
            click.echo(message)
        else:
            click.echo(
                click.style(f"{heading}:", fg="red") + f" {message}", file=sys.stderr
            )

    return success


def messagebox_yesno(message: str, heading: Optional[str] = None) -> bool:
    heading = heading or "I say:"
    if use_gui:
        return tkinter.messagebox.askyesno(heading, message)
    else:
        return click.confirm(message)


def select_engine_installation(engines, initial_id=None):
    if use_gui:
        d = EngineSelector(engines, initial_id)
        return d.result
    else:
        # prompt for the engine root to use using click
        click.echo("Select Engine.  Known engines:")
        keys = desktop.sort_identifiers(engines.keys())
        for i, k in enumerate(keys):
            v = engines[k]
            description = desktop.get_engine_description(k, v, format=True)
            click.echo(
                f"{click.style(f'{i+1}', fg='yellow', reverse=True)}: {description}"
            )
        try:
            initial_idx = keys.index(initial_id) + 1
        except ValueError:
            initial_idx = None
        while True:
            if len(keys):
                prompt = f"Select engine (1 to {len(keys)}) or enter path to engine"
            else:
                prompt = "Enter engine path to engine"
            result = click.prompt(prompt, type=str, default=initial_idx)
            try:
                result = int(result)
                if 1 <= result <= len(keys):
                    return keys[result - 1]
                continue
            except ValueError:
                pass
            if not os.path.exists(result):
                click.echo(
                    f"{click.style('Error:', fg='red')} Path {click.style(result, fg='green')} not found."
                )
                continue
            if desktop.is_valid_root_directory(result):
                return desktop.get_engine_identifier_from_root_dir(result)
            click.echo(
                f"{click.style('Error:', fg='red')} Path {click.style(result, fg='green')} does not contain a valid Unreal Engine."
            )


def main():
    # compatibility with unreal's UnrealVersionSelector.exe
    # the initial command can be prefixed with a single dash or slash
    # so, we remove a  single slask or a dash from the first argument
    # thus found

    for i, arg in enumerate(sys.argv[1:]):
        if arg.startswith("/") or (
            len(arg) > 2 and arg.startswith("-") and not arg.startswith("--")
        ):
            sys.argv[i + 1] = arg[1:]
            break

    tools.click_main(cli, obj={})


if __name__ == "__main__":
    main()
