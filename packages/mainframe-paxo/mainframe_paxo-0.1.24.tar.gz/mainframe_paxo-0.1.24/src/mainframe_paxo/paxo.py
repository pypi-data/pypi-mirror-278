import logging
import os.path
import subprocess
import tempfile
from importlib.metadata import metadata

import click
from click import echo

from . import config, log, p4, tools, ue
from .p4 import p4 as p4_grp
from .ue import ue as ue_grp
from .uvs import uvs as uvs_grp
from .vstudio import vstudio as vstudio_grp

logger = logging.getLogger(__name__)


@click.group(invoke_without_command=True, no_args_is_help=True)
@click.option("--verbose", "-v", is_flag=True, help="Enables verbose mode.")
# @click.option("--version", "-V", is_flag=True, help="Print version and exit.")
@click.version_option()
@click.pass_context
def cli(
    ctx,
    verbose,
):  # version):
    if 0:  # version:
        distribution = metadata("mainframe-paxo")
        click.echo(f"{distribution['Name']} {distribution['Version']}")
        ctx.exit()
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    if verbose:
        log.init()


@cli.command()
def initial_setup():
    click.echo("Welcome to the initial setup of paxo.")
    click.echo(
        """
    Currently this is not automated.  Run the following commands:
    - paxo p4 install
    - paxo p4 setup

    Then, run the following to sync all depots:
    - paxo p4 sync

    Then, set up various UE things:
    - paxo ue setup

    Optionally, Visual Studio:
    - paxo vstudio install

    """
    )


@cli.group()
def self():
    """work with paxo itself."""
    pass


@self.command()
def update():
    """Update paxo."""
    # rye manages our paxo installation
    # to self update, we must create a batch file with the instructions and launch it.abs
    bat_content = """\
@echo off
timeout 1 /nobreak >nul
rye install -f mainframe-paxo
paxo self post-update
timeout 10
"""
    # get a temporary file name to use
    filename = os.path.join(tempfile.gettempdir(), "paxo-update.bat")
    logger.info(f"Writing update bat file to {filename}")
    with open(filename, "w") as f:
        f.write(bat_content)

    # now run it, in detached mode
    # this ensures that we exit and don't get in the way of the bat file
    # file handles must be open, or the timeout commands won't work.
    p = subprocess.Popen(
        f'start cmd.exe /c "{filename}"',
        shell=True,
        # ["cmd", "/c", filename],
        creationflags=subprocess.DETACHED_PROCESS,
        close_fds=False,
    )
    logger.info("%s", p)
    echo(
        "Paxo update started.  Give it a few seconds to complete, then check with 'paxo --version'"
    )


@self.command()
def post_update():
    """Run actions to refresh settings after updating paxo."""
    echo("welcome to post_update_paxo")
    do_location_refresh()


@cli.group()
def location():
    """work with current location"""
    pass


@location.command(name="list")
@click.option("--verbose", "-v", is_flag=True, help="Enables verbose mode.")
def location_list(verbose):
    """list the available locations."""
    echo("Available locations:")
    if not verbose:
        for location in config.locations:
            echo(f" - {location!r} - {config.locations[location]['desc']}")
    else:
        for location, info in config.locations.items():
            echo(f" - {location}")
            for key, value in info.items():
                echo(f"   - {key}: {value}")


@location.command("set")
@click.option(
    "--location",
    prompt="Location",
    type=click.Choice(list(config.locations.keys()), case_sensitive=False),
    default=None,
)
def location_set(location):
    """set the location."""
    p4.set_location(location)
    ue.set_location(location)
    tools.location_set(location)
    echo(f"Location set to {location}")


@location.command("show")
@click.pass_context
def location_show(ctx):
    """show the current location."""
    loc = tools.location_get(empty_ok=True)
    if not loc:
        echo("No location set.  Did you run initial-setup?")
        return
    if ctx.obj["verbose"]:
        echo(f"Current location: {loc}")
        for key, value in tools.locations[loc].items():
            echo(f" - {key}: {value}")
    else:
        echo(loc)


@location.command("refresh")
def location_refresh():
    """refresh location-based settings"""
    do_location_refresh()


def do_location_refresh():
    loc = tools.location_get()
    p4.set_location(loc)
    ue.set_location(loc)
    echo(f"Location {loc} refreshed.")


@cli.group()
def work_drive():
    """Manage work drive."""
    pass


@work_drive.command()
@click.option("--all", "-a", is_flag=True, help="Show all subst drives.")
def show(all):
    """Show the current work drive."""
    if not all:
        drive = tools.work_drive_get()
        echo(f"Currently configured work drive: {drive}")
        drives = [drive]
    else:
        drives = tools.list_subst_drives().keys()
    for drive in drives:
        status = tools.check_subst_drive(drive)
        if not status["subst"]:
            echo(
                f"Drive {drive} currently not active.  use 'paxo work-drive activate' to activate it."
            )
        else:
            echo(f"Drive {drive} points to folder '{status['subst']}'.")
        if not status["reg"]:
            echo(
                f"Drive {drive} currently not permanently registered.  use 'paxo work-drive activate' to map it."
            )


@work_drive.command()
@click.option("--force", "-f", is_flag=True, help="Force activation.")
@click.option("--drive", type=str, help="activate a particular work drive")
def activate(force, drive):
    """Activate the work drive."""
    if drive:
        drive = tools.validate_drivename(drive, check_exists=False)
        tools.work_drive_set(drive)
    tools.subst_drive(force=force)


@work_drive.command()
@click.option("--drive", type=str, help="deactiave a particular work drive")
def deactivate(drive):
    """Deactivate the work drive."""
    if drive:
        drive = tools.validate_drivename(drive, check_exists=True)
        tools.subst_drive(drive, deactivate=True)
    tools.subst_drive(deactivate=True)


@cli.command()
@click.option("--drive", type=click.Path(exists=True, file_okay=False, dir_okay=True))
def data_drive(drive):
    """Select or display the data drive."""
    if drive:
        drive = tools.validate_drivename(drive, check_exists=True)
        tools.data_drive_set(drive)
    else:
        drive = tools.data_drive_get(empty_ok=True)
        if not drive:
            echo("No data drive set.")
            return
    echo(f"Using drive {drive} as data drive.")


@cli.group()
def misc():
    """Miscellaneous commands."""
    pass


@misc.command()
@click.option("--long/--no-long", default=True, help="Enable long filenames.")
def long_filenames(long):
    """Enable long filenames."""
    was = tools.query_long_filenames()
    echo(f"Long filenames are currently {'enabled' if was else 'disabled'}.")
    if long != was:
        try:
            tools.enable_long_filenames(long)
        except PermissionError:
            tools.elevate("Modify the system registry")
            return
        echo(f"Long filenames are now {'enabled' if long else 'disabled'}.")
    else:
        echo("No change made.")


cli.add_command(p4_grp)
cli.add_command(ue_grp)
# no need to manage python after we started using rye
# cli.add_command(python_grp)
cli.add_command(vstudio_grp)
cli.add_command(uvs_grp)


paxo = cli
if __name__ == "__main__":
    tools.click_main(cli, obj={})
