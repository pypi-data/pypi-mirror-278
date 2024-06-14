# utilities for perforce

import contextlib
import datetime
import getpass
import json
import os
import os.path
import socket
import subprocess
import xml.etree.ElementTree as ElementTree

import click
from click import echo

from typing import Optional

from . import tools, winget
from .config import locations

# path prefix for p4 command
p4_prefix = None

# the current user name
p4_user = None

# fingerprints for various p4 servers


def p4_run(args, **kwargs):
    """run a p4 command, and return the output"""

    return p4_run_raw(args, **kwargs)


def p4_json(args, check=True, **kwargs):
    """run a p4 command.  Input and output are dicts"""

    # add options for json input/output
    options = ["-ztag", "-Mj"]

    kwargs["capture_output"] = True

    out = p4_run_raw(options + args, check=check, **kwargs)
    return parse_json_output(out.stdout.decode())


def parse_json_output(data):
    # P4 returns lines of json.  Sometimes there is unparsable data, and we return that
    # as is.
    """json output from p4 is in a line, followed by extra data"""
    result = []
    for line in data.split("\n"):
        if not line:
            continue
        try:
            result.append(json.loads(line))
        except json.JSONDecodeError:
            result.append(line)
    return result


def p4_run_raw(cmd, **kwargs):
    # We have logic here to be able to find p4 even if we just installed it and
    # it is not in the PATH
    global p4_prefix
    if p4_prefix:
        p4 = os.path.join(p4_prefix, "p4.exe")
    else:
        p4 = "p4"

    # inherit and override environment variables
    if "env" in kwargs:
        kwargs["env"] = dict(os.environ, **kwargs["env"])
    try:
        try:
            # print(f"running {cmd} with {kwargs}")
            return subprocess.run([p4] + cmd, **kwargs)
        except FileNotFoundError:
            if p4_prefix:
                raise
            p4_prefix = os.path.join(os.environ["ProgramFiles"], "Perforce")
            p4 = os.path.join(p4_prefix, "p4.exe")
            return subprocess.run([p4] + cmd, **kwargs)
    except FileNotFoundError as e:
        if not have_p4():
            raise click.ClickException(
                "p4 not found.  Have you run 'paxo p4 install'?"
            ) from e
        raise


location_type = click.Choice(list(locations.keys()), case_sensitive=False)


def validate_work_drive(cxt, param, drive: str):
    if len(drive) == 1:
        drive = drive + ":"
    if len(drive) != 2 or drive[1] != ":" or not drive[0].isalpha():
        raise click.BadParameter(
            "work drive must be a single letter followed by a colon"
        )
    if drive.upper() == "P:" or not os.path.isdir(drive):
        raise click.BadParameter(f"{drive} is not a valid drive")
    return drive.upper()


@click.group(chain=True)
def p4():
    """Various Perforce tools for PaxDei development.
    For initial setup use:

    'paxo p4 install setup sync'."""
    pass


@p4.command()
@click.option("--upgrade", is_flag=True, help="upgrade p4 if already installed")
@click.option("--force", is_flag=True, help="force install/upgrade")
def install(force, upgrade):
    """Install/upgrade p4 and p4v"""
    p4_install(force=force, upgrade=upgrade)


@p4.command()
@click.option(
    "--location",
    type=location_type,
    prompt="Specify your location",
    required=True,
    default=lambda: tools.location_get(empty_ok=True),
)
@click.option(
    "--data-drive",
    type=str,
    required=True,
    prompt="Specify your data drive (e.g. D:)",
    callback=validate_work_drive,
    default=lambda: tools.data_drive_get(empty_ok=True),
)
@click.option(
    "--username",
    type=str,
    prompt="Perforce username",
    default=lambda: get_username(),
    help="specify the Perforce user name",
)
@click.option("--force", is_flag=True, help="force setup")
def setup(location, data_drive, username, force):
    """Set up Perforce workspaces for development"""
    p4_setup_dev(location, data_drive, username, force)


@p4.command()
@click.option("--depot", type=str, default="all")
def sync(depot):
    """sync the given depot"""
    all = depot == "all"
    if all:
        msg = "syncing all depots"
    else:
        msg = f"syncing depot '{depot}'"
    print(msg)
    p4_sync(depot, all)
    print(msg + "sync  done")


def p4_install(force=False, upgrade=False):
    """Initial setup of p4 for PaxDei development"""
    print("Installing P4 and P4V")

    # optionally install p4
    version = have_p4()
    if version:
        print(f"current p4 version {version}")
        if not upgrade or force:
            print("Not installing. use --upgrade to upgrade")
            return
    print("p4 not found")
    version = install_p4(force=force, upgrade=upgrade)
    print(f"p4 version {version}")

    # various settings
    p4_set_various()

    # fixup p4v settings
    fix_p4v_settings()


def install_p4(force=False, upgrade=False):
    version = have_p4()
    winget.install("Perforce.P4V", force=force, upgrade=upgrade)
    if not version:
        # we just installed it, and want it in the path
        tools.addpath(os.path.join(os.environ["ProgramFiles"], "Perforce"))
    return have_p4()


def p4_setup_dev(location, data_drive, username, force=False):
    # set p4port and p4trust
    tools.location_set(location)
    set_location(location)

    p4_set_user(username)

    # create the subst
    tools.subst_drive(data_drive, force=True)

    # set the client to the paxdei depot by default
    p4client_set(get_client_name("paxdei", no_legacy=True))

    # login
    do_login(quiet=True)

    legacy = discover_legacy_clients()

    # create the client specs
    tools.data_drive_set(data_drive)
    for depot in ["paxdei", "UE"]:
        if depot in legacy and not force:
            name = legacy[depot]["client"]
            echo(f"Adopting existing client {name} for depot {depot}")
            echo("to create a new workspace instead, use 'paxo p4 setup --force'.")
        else:
            name = do_create_client(depot)
            echo("creating / updating client " + name)
        tools.env_var_set(f"PD_CLIENT_{depot}", name)


@p4.command()
def show():
    """Show the current workspaces"""
    echo("Current workspaces:")
    names = ["paxdei", "UE"]
    for name in names:
        client = get_existing_client_name(name)
        if client:
            echo(f"  {name}: {client}")
            info = get_client_info(client)
            echo(f'    Root: {info["Root"]}, Stream: {info["Stream"]}')
        else:
            echo(f"  {name}: no client found")


@p4.command()
def get_version():
    """Get the version of the installed Perforce client."""
    version = have_p4()
    if version:
        print(f"p4 version {version}")
    else:
        print("p4 not found")


def do_login(quiet=False):
    username = p4_set_get()["P4USER"]
    out = p4_run(["login", "-s"], capture_output=True)
    if out.returncode == 0:
        if not quiet:
            print(
                f"User '{username}' already logged in. " + out.stdout.decode().strip()
            )
        return True

    print(
        f"Not logged in.  Attempting login for user '{username}'. Enter password and look for a JumpCloud notification on your phone."
    )
    out = p4_run(["login"])
    if out.returncode != 0:
        print("login failed.")
        print(
            "If the above message says that your account 'has not been enabled', please contact #it_helpdek"
        )
        print("to have your account enabled for Perforce access, before retrying.")
        raise click.ClickException("login failed")

    return out.returncode == 0


@p4.command()
def trust_all():
    """Update p4 trust for all locations"""
    set_p4trust(verbose=True)


def set_location(location):
    set_p4port(location, verbose=True)
    set_p4trust(location, verbose=True)


def get_p4port(location):
    """return a suitable value for P4PORT"""
    return locations[location]["p4port"]


def set_p4port(location: str, verbose: Optional[bool] = False):
    p4port = get_p4port(location)
    set_current_p4port(p4port, verbose=verbose)


def get_current_p4port():
    out = p4_run(["set", "P4PORT"], capture_output=True, check=True)
    port = out.stdout.decode().strip().split("=")[1].split()[0]
    click.echo(f"Current P4PORT is {port}")
    return port


def set_current_p4port(port: str, verbose: Optional[bool] = False):
    if verbose:
        click.echo(f"Setting P4PORT to {port}")
    p4_run(["set", f"P4PORT={port}"], check=True)


@contextlib.contextmanager
def p4port_ctx(location: Optional[str] = None, port: Optional[str] = None):
    """Context manager for setting the P4PORT"""
    old_port = get_current_p4port()
    if port:
        set_current_p4port(port)
    elif location:
        set_p4port(location)
    try:
        yield
    finally:
        set_current_p4port(old_port)


def get_p4trust(location):
    """return a suitable value for P4TRUST"""
    loc = locations[location]
    return loc["p4trust"]


def set_p4trust(location: Optional[str] = None, verbose: Optional[bool] = False):
    """Set the P4TRUST value, either of a single region or all"""
    if location:
        if verbose:
            click.echo(f"Setting p4 trust for {location}")
        p4trust = get_p4trust(location)
        with p4port_ctx(location):
            try:
                p4_run(["trust", "-f", "-i", p4trust], check=True, timeout=3)
            except subprocess.TimeoutExpired:
                click.echo(
                    f"Trust request timed out, possibly you can't access location {location} ({get_p4port(location)}) from here."
                )
    else:
        for loc in locations:
            set_p4trust(loc, verbose=verbose)


def have_p4():
    version = None
    try:
        output = p4_run(["-V"], capture_output=True, check=True)
        for line in output.stdout.decode().split("\n"):
            if line.startswith("Rev."):
                version = line.split()[1].split("/")[2]
                break
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass

    return version


def p4_set_various():
    """Set various p4 options"""
    p4_run(["set", "P4CHARSET=utf8"])
    p4_run(["set", "P4COMMANDCHARSET=utf8"])
    p4_run(["set", "P4CONFIG=.p4config.txt;.p4config;p4config.txt"])
    p4_run(["set", "P4IGNORE=.p4ignore.txt;.p4ignore;p4ignore.txt"])


def p4_set_get():
    out = p4_run(["set"], capture_output=True, check=True)
    result = {}
    for line in out.stdout.decode().split("\n"):
        line = line.strip()
        if not line:
            continue
        # remove the trailing () comment
        line = line.rsplit(" ", 1)[0]
        key, value = line.split("=", 1)
        result[key] = value
    return result


def p4_set_user(user):
    """Set the user name"""
    global p4_user
    user = user or getpass.getuser()
    p4_run(["set", f"P4USER={user}"])
    p4_user = user


@p4.command()
@click.option("--depot", type=str, prompt="Specify the depot")
def create_client(depot):
    """create a new client for the given depot"""

    do_create_client(depot)


def do_create_client(depot, stream="main"):
    # Our standard clients are rooted at the W drive directly.

    client_name = get_client_name(depot, no_legacy=True)
    client_root = os.path.normpath(os.path.join(tools.work_drive_get(), "/", depot))
    date = datetime.datetime.now(tz=datetime.timezone.utc).strftime(
        "%Y/%m/%d %H:%M:%S %Z"
    )
    options = "rmdir"
    if depot == "UE":
        options += " allwrite"

    client_spec = f"""
Client: {client_name}
Owner: {get_username()}
Host: {get_hostname()}
Description:
 Created by paxo on {date}
Root: {client_root}
Options: {options}
Stream: //{depot}/{stream}
View:
 //{depot}/{stream}/... //{client_name}/...
"""
    print(client_spec)
    os.makedirs(client_root, exist_ok=True)
    p4_run(["client", "-i"], input=client_spec.encode(), check=True)
    write_p4config(client_name, client_root)
    return client_name


def write_p4config(client_name, client_root):
    p4config = f"""
P4CLIENT={client_name}
"""
    with open(os.path.join(client_root, ".p4config"), "w") as f:
        f.write(p4config)


def get_client_name(depot, postfix=None, no_legacy=False):
    """return a suitable client name for the given stream"""
    if not no_legacy:
        name = get_existing_client_name(depot)
        if name:
            return name
    name = f"pd.{get_username()}.{get_hostname()}.{depot}"
    if postfix:
        name += f".{postfix}"
    return name


def get_existing_client_name(depot):
    """return the name of the existing client for the given depot"""
    return tools.env_var_get(f"PD_CLIENT_{depot}")


def get_hostname():
    return socket.gethostname()


def get_username():
    # we want to use the same username as perforce uses in p4user
    # but if that is not set, use the current user
    global p4_user
    if p4_user:
        return p4_user
    user = p4_set_get()["P4USER"]
    if not user:
        user = getpass.getuser()
    p4_user = user
    return user


def p4client_set(client):
    """set the current client"""
    p4_run(["set", f"P4CLIENT={client}"], check=True)


def p4client_get():
    """get the current client"""
    out = p4_run(["set", "P4CLIENT"], check=True, capture_output=True)
    return out.stdout.decode().strip().split("=")[1].split()[0]


@contextlib.contextmanager
def p4client(client):
    """context manager for setting the current client"""
    old_client = p4client_get()
    p4client_set(client)
    try:
        yield
    finally:
        p4client_set(old_client)


def p4_sync(depot="paxdei", all=False):
    if all or depot == "all":
        depots = ["paxdei", "UE"]
    else:
        depots = [depot]
    for d in depots:
        client = get_client_name(depot=d)
        with p4client(client):
            p4_run(["sync"], check=True)


@p4.command()
@click.option("--depot", type=str, default="paxdei")
@click.argument("stream-name")
def switch(depot, stream_name):
    """switch to the given stream"""
    depots = ["paxdei", "UE"]
    use_fallback = "paxdei" in depots
    fallback = "main"
    rollback = []
    fail = False
    try:
        for d in depots:
            # fallback to main if the stream doesn't exist and we are not paxdei
            current_fallback = fallback if use_fallback and d != "paxdei" else None
            previous_stream = get_client_stream(get_client_name(d))
            result = p4_switch(d, stream_name, fallback=current_fallback)
            if result:
                rollback.append((stream_name, previous_stream))
            else:
                fail = True
                break
        else:
            # we succeeded in switching all depots
            rollback = []
    finally:
        # rollback if we failed
        for depot, previous_stream in reversed(rollback):
            p4_switch(depot, previous_stream)

    return not fail


def p4_switch(depot, stream_name, fallback=None, no_sync=True):
    """switch to the given stream"""

    streams = find_streams(depot)
    if stream_name not in streams:
        if fallback and fallback in streams:
            print(
                f"stream {stream_name} not found for depot {depot}.  Using {fallback} instead"
            )
            stream_name = fallback
        else:
            print(f"stream {stream_name} not found for depot {depot}.")
            return False

    client = get_client_name(depot)
    current_stream = get_client_stream(client)
    print(depot, stream_name, "1")
    if current_stream == stream_name:
        print(f"client {client} is already on stream '{stream_name}'")
        return True

    cmd = ["switch", stream_name]
    if no_sync:
        cmd.insert(1, "--no-sync")
        print(cmd)
    res = p4_run(cmd, check=False, env={"P4CLIENT": client})
    print(depot, stream_name, "2")
    if res.returncode == 0:
        print(f"client {client} switched to stream '{stream_name}'")
        return True
    return res.returncode != 0


@p4.command()
@click.option("--depot", type=str, default="paxdei")
def stream(depot):
    """display the current stream"""

    client = get_client_name(depot)
    current_stream = get_client_stream(client)
    print(f"client {client} is on stream '{current_stream}'")


def get_client_info(client):
    """return the client info for the given client"""
    out = p4_json(["client", "-o", client])
    return out[0]


def get_client_stream(client):
    """return the stream for the given client"""
    out = p4_json(["switch"], env={"P4CLIENT": client})
    return out[0]["data"]


def fix_p4v_settings():
    # fix the p4v xml settings file
    filename = os.path.join(
        os.environ["USERPROFILE"], ".p4qt", "ApplicationSettings.xml"
    )

    if os.path.isfile(filename):
        tree = ElementTree.parse(filename)
        root = tree.getroot()
        for elem in root.iter():
            if (
                elem.tag == "String"
                and elem.attrib.get("varName", "") == "DefaultCharset"
            ):
                elem.text = "utf8-bom"
        tree.write(filename, encoding="utf-8")
    else:
        # create new settings with only this content.
        root = ElementTree.Element(
            "PropertyList",
            attrib={"IsManaged": "TRUE", "varName": "ApplicationSettings"},
        )
        elem = ElementTree.SubElement(
            root, "PropertyList", attrib={"IsManaged": "TRUE", "varName": "Connection"}
        )
        elem = ElementTree.SubElement(
            elem, "String", attrib={"varName": "DefaultCharset"}
        )
        elem.text = "utf8-bom"
        tree = ElementTree.ElementTree(root)
        ElementTree.indent(tree, " ")
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        tree.write(filename, encoding="utf-8")


@p4.command()
@click.option("--depot", type=str, default="paxdei")
def streams(depot):
    """list the streams in the given depot"""
    streams = find_streams(depot)
    for stream in streams:
        print(stream)


def find_streams(depot):
    """return a list of streams in the given depot"""
    client = get_client_name(depot)
    out = p4_json(["switch", "-l"], env={"P4CLIENT": client})
    return [line["data"].split()[0] for line in out]


def get_engine_path():
    """Return the root path of the engine"""
    client = get_client_name(depot="UE")
    client_info = get_client_info(client)
    return client_info["Root"]


@p4.command()
def discover():
    """Discover the clients already set up for this host and user"""

    print("Discovering clients")
    print(discover_legacy_clients())


def discover_legacy_clients():
    """
    Return the most recently used and valid clients for this host and user,
    first for the PaxDei depot and then for the UE depot.
    """
    result = {}
    out = p4_json(["clients", "-u", get_username()])
    if not out:
        return result
    host = get_hostname()
    # Filter for this host and sort by reverse access time (most recent first)
    clients = [client for client in out if client["Host"] == host]
    clients.sort(key=lambda c: c["Access"], reverse=True)
    clients = [c for c in clients if os.path.isdir(c["Root"])]
    clients = [c for c in clients if "Stream" in c]

    # filter away automatically generated client names, to leave only legacy clients
    clients = [c for c in clients if not c["client"].startswith("pd.")]

    names = ["paxdei", "UE"]
    for n in names:
        c = [c for c in clients if c["Stream"].startswith(f"//{n}/")]
        if c:
            result[n] = c[0]
    return result

    pd = [c for c in clients if c["Stream"].startswith("//paxdei/")]
    ue = [c for c in clients if c["Stream"].startswith("//UE/")]

    return (pd[0] if pd else None, ue[0] if ue else None)
