import glob
import json
import os.path
import shlex
import subprocess
import sys
import winreg
from contextlib import contextmanager

import click
from click import echo, secho

from . import config, p4, tools, uvs
from .registry import Key
from .uebase import desktop
from .uebase.desktop import is_valid_root_directory


# helper to close winreg keys
@contextmanager
def close_key(key):
    try:
        yield key
    finally:
        key.Close()


# various tools for setting up UE environment and running it.abs


@click.group()
@click.pass_context
def ue(ctx):
    """work with Unreal Engine"""


@ue.group()
def env():
    """Unreal environment variables, DDC, etc."""


@env.command()
def show():
    """Show current Env var settings"""
    loc = tools.location_get()
    echo(f"Location is set to {loc}")

    def report(var, val, should, description):
        echo(description)
        if val is not None:
            secho(f"  {var}={val}", fg="green")
        else:
            secho(f"  {var} is not set", fg="yellow")
        if should is not None and val != should:
            secho(f"  '{var}' is not set to the expected value '{should}'", fg="red")

    for place, var in [
        ("Local", "UE-LocalDataCachePath"),
        ("Shared", "UE-SharedDataCachePath"),
    ]:
        description = f"{place} data cache path:"
        if place == "Shared":
            should = config.locations[loc]["ddc"]
        else:
            should = None
        report(var, tools.env_var_get(var), should, description)

    # display the git dependencies cache path
    var, should, path = get_gitdeps_var()
    report(var, tools.env_var_get(var), should, "Git dependencies cache path:")


@env.command()
def test():
    """Test the current DDC settings"""

    def report(var, val, should_be_local, description):
        drive, path = os.path.splitdrive(val)
        islocal = tools.validate_drivename(drive, check_exists=False)
        if not islocal and should_be_local:
            secho(
                f"{description} drive '{drive}' for '{val}' does not exist.", fg="red"
            )
        elif islocal and not should_be_local:
            secho(
                f"{description} drive '{drive}' for '{val}' appears to be local",
                fg="red",
            )
        if not os.path.isdir(drive):
            secho(
                f"{description} drive '{drive}' for '{val}' is not accessible", fg="red"
            )
        else:
            secho(f"{description} path '{val}' exists", fg="green")

    for place, var in [
        ("Local", "UE-LocalDataCachePath"),
        ("Shared", "UE-SharedDataCachePath"),
    ]:
        val = tools.env_var_get(var)
        if val is None:
            continue
        report(var, val, place == "Local", f"{place} data cache")

    var, _, path = get_gitdeps_var()
    val = tools.env_var_get(var)
    if val is not None:
        report(var, path, True, "Git dependencies cache")


@env.command()
@click.option("--force", is_flag=True, help="Reset even those with a valid value")
def set(force: bool) -> None:
    """Set the environment variables for the current location"""
    settings = [
        get_local_data_cache_path(),
        get_shared_data_cache_path(),
        get_gitdeps_var()[:2],
    ]
    for var, val in settings:
        current = tools.env_var_get(var)
        if current is None or current != val:
            if not force and not click.confirm(
                f"Override {var}={current} with '{val}'?", default=False
            ):
                continue
            tools.env_var_set(var, val)
            echo(f"Set {var}={val}")
        else:
            echo(f"{var}={val} already set")


@ue.group()
@click.option(
    "--engine-path",
    type=click.Path(exists=False),
    default=lambda: p4.get_engine_path(),
    help="The path to register if not default engine path.",
)
@click.option(
    "--scope",
    type=click.Choice(["user", "machine"]),
    default="user",
    help="Work with user or machine registry",
)
@click.option(
    "--check/--no-check", is_flag=True, help="Only accept valid engine paths."
)
@click.pass_context
def engine(ctx, engine_path, scope, check):
    """work with engine registration"""
    ctx.ensure_object(dict)
    ctx.obj["engine_path"] = engine_path
    ctx.obj["scope"] = scope
    ctx.obj["reg_root"] = (
        winreg.HKEY_CURRENT_USER if scope == "user" else winreg.HKEY_LOCAL_MACHINE
    )
    ctx.obj["check"] = check


@ue.command()
def setup():
    """Set up the environment for Unreal Engine development."""
    setup_ue(tools.data_drive_get(), p4.get_engine_path(), tools.location_get())


@engine.command("register")
@click.pass_context
@click.option("--engine-id", type=str, metavar="<id-string>", default=None)
def engine_register(ctx, engine_id):
    check = ctx.obj["check"]
    register_engine(ctx.obj["engine_path"], engine_id, check=check)


@engine.command("deregister")
@click.argument("engine-id", type=str, metavar="<id-string>")
@click.pass_context
def engine_deregister(ctx, engine_id):
    deregister_engine(ctx.obj["engine_path"], engine_id)


@engine.command("list")
@click.pass_context
@click.option("--all", is_flag=True, help="List both user and machine registrations.")
def engine_list(ctx, all):
    user = ctx.obj["scope"] == "user"
    if user or all:
        print("User registered engines:")
        reg_root = winreg.HKEY_CURRENT_USER
        with Key(reg_root, "SOFTWARE\\Epic Games\\Unreal Engine\\Builds") as key:
            for name, value in key.items():
                print(f"{name} = {value[0]}")
    if not user or all:
        print("System registered engines:")
        reg_root = winreg.HKEY_LOCAL_MACHINE
        key = Key(reg_root, "SOFTWARE\\EpicGames\\Unreal Engine")
        if key:
            with key:
                for subkey in key.subkeys():
                    with subkey:
                        print(f"{subkey.name} = {subkey['InstalledDirectory']}")


@engine.command("lookup")
@click.pass_context
@click.argument("engine-id", type=str, metavar="<id-string>")
@click.option(
    "--all/--no-all",
    is_flag=True,
    default=True,
    help="Look up in both user and machine registrations.",
)
def engine_lookup(ctx, engine_id, all, check):
    user = ctx.obj["scope"] == "user"
    path = None
    if user or all:
        reg_root = winreg.HKEY_CURRENT_USER
        with Key(reg_root, "SOFTWARE\\Epic Games\\Unreal Engine\\Builds") as key:
            if key:
                path = key.get(engine_id, None)
    if path is not None and check and not is_valid_root_directory(path):
        path = None
    if path is None and (not user or all):
        reg_root = winreg.HKEY_LOCAL_MACHINE
        with Key(reg_root, "SOFTWARE\\EpicGames\\Unreal Engine") as key:
            if key:
                for subkey in key.subkeys():
                    with subkey:
                        if subkey.name == engine_id:
                            path = subkey["InstalledDirectory"]
                            break
    if path is not None and check and not is_valid_root_directory(path):
        path = None

    if path is not None:
        echo(path)
    sys.exit(1)


@ue.group()
@click.option("--scope", type=click.Choice(["user", "machine"]), default="user")
@click.pass_context
def fileassociations(ctx, scope):
    """work with .uproject files registration"""
    ctx.ensure_object(dict)
    ctx.obj["scope"] = scope


@fileassociations.command("set")
@click.pass_context
@click.option(
    "--engine-path",
    type=click.Path(exists=False),
    default=lambda: p4.get_engine_path(),
    help="The path to the handling Engine if not the default path.",
)
@click.option(
    "--handler",
    type=click.Path(exists=False),
    default=None,
    help="The path of a custom handler executable to use.",
)
@click.option(
    "--self/--no-self", default=True, help="Use the current script as handler."
)
def uproject_register(ctx, engine_path, handler, self):
    user = ctx.obj["scope"] == "user"
    if self and not handler:
        handler = uvs.find_run_args(gui=True)
        engine_path = None
    else:
        if handler:
            handler = [handler]
        else:
            if not engine_path:
                engine_path = p4.get_engine_path()
    uvs.update_file_associations(user=user, engine_root=engine_path, handler=handler)
    return


@fileassociations.command("get")
@click.pass_context
@click.option(
    "--verify/--no-verify", default=True, help="Verify that target files exist."
)
def uproject_get(ctx, verify):
    ctx.invoke(uvs.fileassociations, check=True)


@fileassociations.command("clear")
@click.pass_context
def uproject_deregister(ctx):
    user = ctx.obj["scope"] == "user"
    deregister_uproject_handler(user=user)


def setup_ue(data_drive: str, engine_path: str, location: str | None = None) -> None:
    # enable long filenames
    enable_long_filenames()

    # set up the environment variables
    set_ddc_vars(data_drive, location)

    # set the file associations to use the uvs module
    uvs.update_file_associations(user=True)

    # register the engine
    if not os.path.isfile(os.path.join(engine_path, "build_info.json")):
        raise click.ClickException(
            f"Engine path {engine_path} does not contain an engine.  Have you performed a sync?"
        )
    engine_id = get_engine_id_from_build_info(engine_path)
    uvs.register_current_engine_directory(engine_root=engine_path, engine_id=engine_id)

    # install prerequisites
    install_prerequisites(engine_path)


def set_location(location: str) -> None:
    # set the env vars related to location
    var, ddc = get_shared_data_cache_path(location)
    if ddc:
        print(f"setting shared data cache path to {ddc} for location {location}")
        tools.env_var_set(var, ddc)
    else:
        print(f"clearing shared data cache path for location {location}")
        tools.env_var_del(var)


def get_gitdeps_var(data_drive: str | None = None) -> tuple[str, str, str]:
    """Get the environment variable for the gitdeps folder."""
    drive = data_drive or tools.data_drive_get(empty_ok=False)
    path = os.path.join(drive, config.data_drive_git_depends)
    return "UE_GITDEPS_ARGS", f"--cache={path}", path


def get_local_data_cache_path(data_drive: str | None = None) -> tuple[str, str]:
    """Get the local data cache path."""
    drive = data_drive or tools.data_drive_get(empty_ok=False)
    return "UE-LocalDataCachePath", os.path.join(drive, config.data_drive_ddc_folder)


def get_shared_data_cache_path(location: str | None = None) -> tuple[str, str | None]:
    """Get the shared data cache path."""
    loc = location or tools.location_get()
    return "UE-SharedDataCachePath", config.locations[loc]["ddc"]


def set_ddc_vars(data_drive, location):
    # set local DDC location
    var, path = get_local_data_cache_path(data_drive)
    print(f"setting local data cache path to {path}")
    tools.env_var_set(var, path)

    # additionally, the git dependencies for source engines are cached
    # in the same place
    print(f"setting git dependencies cache path to {path}")
    var, value, path = get_gitdeps_var(data_drive)
    tools.env_var_set(var, value)


def get_uproject_handler(user=True, verify=True):
    reg_root = winreg.HKEY_CURRENT_USER if user else winreg.HKEY_LOCAL_MACHINE

    def unquote(s):
        if s[0] == '"' and s[-1] == '"':
            s = s[1:-1]
        return s

    def check_handler(s, verify=False):
        parts = shlex.split(s)
        if not os.path.isfile(parts[0]):
            print(f"Warning: {parts[0]} does not exist")
            if verify:
                raise click.ClickException(f"Could not find {parts[0]}")

    # we must now find the appropriate place in the registry and add it.abs
    # this is a bit tricky, but we can use the python winreg module
    with Key(reg_root, "SOFTWARE\\Classes\\.uproject") as key:
        if not key:
            return None
        cls = key[""]
        if not cls:
            return None

    with Key(reg_root, f"SOFTWARE\\Classes\\{cls}") as key:
        if not key:
            return None

        exe = key.get("VersionSelectorExecutable")
        if exe:
            return unquote(exe)

        # look for the "open" subkey
        with key.subkey(r"shell\open\command") as subkey:
            if not subkey:
                return None
            cmd = subkey[""]
            # we expect something like '"C:\Program Files\Epic Games\UE_4.26\Engine\Binaries\Win64\UnrealVersionSelector.exe" /editor "%1"'
            # split it into the exe and the args, taking care of quotes, ignoring spaces inside the quotes
            parts = cmd.split('"')
            return parts[1]


def deregister_uproject_handler(user=True):
    # the engine contains a special execution to act as a shell handler
    # for files with the .uproject extension
    reg_root = winreg.HKEY_CURRENT_USER if user else winreg.HKEY_LOCAL_MACHINE

    Key(reg_root, "SOFTWARE\\Classes\\Unreal.ProjectFile").delete(tree=True)
    Key(reg_root, "SOFTWARE\\Classes\\.uproject").delete(tree=True)
    if user:
        Key(
            reg_root,
            "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\FileExts\\.uproject\\UserChoice",
        ).delete(tree=True)


def get_engine_id_from_build_info(engine_path, check=True):
    # read the engine registry name from the build_info.json file
    check = True

    if check and not is_valid_root_directory(engine_path):
        raise click.ClickException(f"Engine path {engine_path} is not valid")

    try:
        with open(os.path.join(engine_path, "build_info.json")) as f:
            info = json.load(f)
        return info["engine_id"]
    except OSError:
        return None


def register_engine(engine_path, engine_id=None, check=True):
    # read the engine registry name from the build_info.json file

    if check and not is_valid_root_directory(engine_path):
        raise click.ClickException(f"Engine path {engine_path} is not valid")

    if not engine_id:
        with open(os.path.join(engine_path, "build_info.json")) as f:
            info = json.load(f)
        engine_name = info["engine_id"]
    else:
        engine_name = engine_id

    # now open the registry key for the user
    key = Key(winreg.HKEY_CURRENT_USER, "SOFTWARE\\Epic Games\\Unreal Engine\\Builds")
    with key.create():
        key[engine_name] = engine_path


def deregister_engine(engine_path=None, engine_id=None):
    if not engine_path and not engine_id:
        raise ValueError("Must specify either engine_path or engine_id")
    if not engine_id:
        assert not engine_id
        with open(os.path.join(engine_path, "build_info.json")) as f:
            info = json.load(f)
        engine_id = info["engine_id"]
    with Key(
        winreg.HKEY_CURRENT_USER,
        "SOFTWARE\\Epic Games\\Unreal Engine\\Builds",
        write=True,
    ) as key:
        if key:
            del key[engine_id]


def register_engine_old(engine_path):
    # we have a special engine registration tool in the engine folder
    tool = os.path.join(engine_path, "build-tools", "register_engine.cmd")
    subprocess.check_call([tool])


def install_prerequisites(engine_path):
    # we have a special engine registration tool in the engine folder
    tool = os.path.join(
        engine_path, "Engine", "Extras", "Redist", "en-us", "UEPrereqSetup_x64.exe"
    )
    click.echo(f"Installing prerequisites for the engine from {tool!r}")
    subprocess.check_call([tool, "/quiet"])


def start_editor(engine_path, project_path):
    # find the .uproject file in project_path
    uproject = glob.glob(os.path.join(project_path, "*.uproject"))[0]
    uproject = os.path.abspath(uproject)

    # find the ue executable
    ue = os.path.join(engine_path, "Engine", "Binaries", "Win64", "UnrealEditor.exe")

    # start the editor
    subprocess.check_call([ue, uproject])


# uproject engine registration stuff


def read_uproject(uproject):
    # read the .uproject file
    with open(uproject) as f:
        info = json.load(f)
    return info


def write_uproject(uproject, info):
    # write the .uproject file
    with open(uproject, "w") as f:
        json.dump(info, f, indent="\t")


def get_engine_association(uproject):
    # read the .uproject file
    info = read_uproject(uproject)
    engine = info.get("EngineAssociation", None)
    return engine


def set_engine_association(uproject, engine_identifier):
    # read the .uproject file
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
    write_uproject(uproject, info)


def find_engine_for_project(uproject):
    """Finds the root of the engine to use for this uproject file"""
    engine_id = get_engine_association(uproject)
    if not engine_id:
        # this is a unified build, so we need to find the engine in
        # the parents
        return find_engine_in_parents(uproject)
    else:
        # guids are not engine paths, bypass the engine path test
        if not is_ue_engine_guid(engine_id):
            # first, check if the id is in fact a file path.
            # does it look like a path?  If it is not an absolute path, try to
            # use it relative to the project root
            engine_path = engine_id
            if not os.path.isabs(engine_path):
                engine_path = os.path.join(os.path.dirname(uproject), engine_id)
            if is_valid_root_directory(engine_path):
                return engine_path

        # no, not an engine path.  It must be an id, then.
        return look_up_engine(engine_id)


def is_ue_engine_guid(guid):
    """Check if this is a valid engine guid"""
    # unreal guids are 38 chars, hex digits, with dashes
    if len(guid) != 38:
        return False
    if not guid.startswith("{") and not guid.endswith("}"):
        return False
    return True


def find_engine_in_parents(uproject):
    """Given an uproject, search up the hierarhcy until an engine is found"""
    uproject = os.path.abspath(uproject)
    project_folder = os.path.dirname(uproject)
    current = os.path.dirname(project_folder)
    last = ""
    # loop until we can reach no higher
    while current != last:
        last = current
        # check if this folder contains an engine
        if is_valid_root_directory(current):
            # found the engine
            return current
        # go up a level
        current = os.path.dirname(current)


def look_up_engine(engine_id):
    """Look up the engine path from the registry"""
    engines = desktop.platform.enumerate_engine_installations()
    return engines.get(engine_id, None)


def get_editor_path(engine_path):
    """Get the path to the editor executable"""
    editor = os.path.join(
        engine_path, "Engine", "Binaries", "Win64", "UnrealEditor.exe"
    )
    if os.path.isfile(editor):
        return editor


def get_editor_from_uproject(uproject):
    """Get the path to the editor executable from the uproject file"""
    engine_path = find_engine_for_project(uproject)
    if not engine_path:
        return None
    return get_editor_path(engine_path)


def enable_long_filenames() -> None:
    was = tools.query_long_filenames()
    echo(f"Long filenames are currently {'enabled' if was else 'disabled'}.")
    if was:
        return
    echo("Enabling long filenames.")
    try:
        tools.enable_long_filenames(True)
    except PermissionError:
        tools.elevate(
            reason="enable long filenames", args=["misc", "long-filenames", "--long"]
        )
        return
