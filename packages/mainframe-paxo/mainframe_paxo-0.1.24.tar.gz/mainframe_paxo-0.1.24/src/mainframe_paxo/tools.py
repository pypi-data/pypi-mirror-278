import os
import shlex
import subprocess
import sys
import tkinter.messagebox
import ctypes

import click

from . import config
from .registry import Key
from typing import Optional

# some common environment tools for us


def validate_drivename(drivename, check_exists=True):
    if drivename.startswith("\\\\"):
        return False
    drivename = drivename.upper().strip()
    if not drivename.endswith(":"):
        drivename += ":"
    if check_exists:
        if not os.path.isdir(os.path.join(drivename, "\\")):
            raise ValueError(f"Drive {drivename} does not exist")
    return drivename


# data_drive is the pyhysical drive we use for storage.
# we then use subst to map the paxdei_dev folder to a different drive letter
# typically W:  This is the work drive.


def data_drive_set(drivename):
    drivename = validate_drivename(drivename)
    env_var_set("PD_DATA_DRIVE", drivename)
    env_var_del("PD_WORKDRIVE")


def data_drive_get(empty_ok=False):
    drivename = env_var_get("PD_DATA_DRIVE")
    drivename = drivename or env_var_get("PD_WORKDRIVE")  # backwards compatibility
    if not drivename and not empty_ok:
        raise ValueError("PD_DATA_DRIVE not set.  Did you run initial-setup?")
    if not drivename and empty_ok:
        return None
    return validate_drivename(drivename, check_exists=False)


# work location related stuff
def location_set(location):
    if location not in config.locations.keys():
        raise ValueError(f"Unknown location {location}")
    env_var_set("PD_LOCATION", location)


def location_get(empty_ok=False):
    location = env_var_get("PD_LOCATION")
    if not location:
        if empty_ok:
            return None
        raise ValueError("PD_LOCATION not set.  Did you run initial-setup?")
    if location not in config.locations.keys():
        raise ValueError(f"Unknown location {location}")
    return location


# setting and getting environment variables
def env_var_get(name):
    if name in os.environ:
        return os.environ[name]

    # the env var may have been set in a previous session
    # and not yet updated in _out_ environment. so we look
    # in the registry.
    with Key.current_user("Environment") as key:
        value = key.get(name, None)
        if value:
            return value
    # try the system environment
    with Key.local_machine(
        "SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment"
    ) as key:
        return key.get(name, None)


def env_var_set(name, value, permanent=True, system=False):
    if permanent:
        cmd = ["setx", name, value]
        if system:
            cmd.append("/m")
        subprocess.run(cmd, check=True, capture_output=True)
    os.environ[name] = value


def env_var_del(name, permanent=True, system=False):
    if not permanent:
        try:
            del os.environ[name]
        except KeyError:
            pass
    if not permanent:
        return

    if not system:
        key = Key.current_user("Environment")
    else:
        key = Key.local_machine(
            "SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment"
        )
    with key.open(write=True):
        try:
            del key[name]
        except KeyError:
            pass


def addpath(path, permanent=False, system=False, infront=False):
    if infront:
        path = path + ";" + os.environ["PATH"]
    else:
        path = os.environ["PATH"] + ";" + path
    env_var_set("PATH", path, permanent, system)


# Subst!  This is a key feature of paxo.
# The user selects a a data drive, e.g. D:, with plenty of room.
# We then ensure that it has a folder called D:\paxdei_dev, and
# we subst that to W:\


def subst_drive(data_drive=None, force=False, permanent=True):
    """Subst the paxdei root folder to the work-drive drive"""
    # W will have the structure
    # W:\.paxo   # this is a marker file to identify it.
    # W:\paxdei
    # W:\UE
    # W:\otherstuff

    data_drive = data_drive or data_drive_get(empty_ok=False)
    work_drive = work_drive_get()

    if subst_drive == "P:":
        raise ValueError(
            "Drive P: is reserved for Pipeline.  Please select another drive."
        )
    if data_drive == work_drive:
        raise ValueError(
            "You must have a different drive letter for work drive and data drive.  Call for help."
        )

    # ensure the src folder exists
    src = os.path.join(data_drive, config.data_drive_dev_folder)
    os.makedirs(src, exist_ok=True)

    # ensure that it contains the .paxo file
    with open(os.path.join(src, ".paxo"), "w") as f:
        f.write("This is the paxo work drive")

    out = subprocess.run(["subst", work_drive, src], capture_output=True)
    if out.returncode == 0:
        data_drive_set(data_drive)
        if permanent:
            register_subst_drive(work_drive, src)
        return True

    if "already" not in out.stdout.decode():
        out.check_returncode()

    if force:
        subprocess.run(["subst", work_drive, "/d"], check=True)
        subprocess.run(["subst", work_drive, src], check=True)
        data_drive_set(data_drive)
        if permanent:
            register_subst_drive(work_drive, src)
        return True
    return False


def list_subst_drives():
    """List all subst drives"""
    out = subprocess.run(["subst"], capture_output=True)
    result = {}
    for line in out.stdout.decode().splitlines():
        drive, target = line.split("=>")
        drive = drive.strip()[:2]
        result[drive] = target.strip()
    return result


def check_subst_drive(drive):
    """See if a drive is currently subst"""
    out = subprocess.run(["subst"], capture_output=True)
    is_subst = False
    for line in out.stdout.decode().splitlines():
        if line.startswith(drive):
            target = line.split("=>")[1].strip()
            is_subst = target

    registered = get_registered_subst_drives()
    is_reg = registered.get(drive, False)
    return {"subst": is_subst, "reg": is_reg}


# To make subst permanent, we need to add that command to the windows run registry to be executed on every login


def register_subst_drive(drive, src):
    """Register a subst drive in the registry"""
    cmd = shlex.join(["subst", drive, src])
    name = f"paxo-subst-{drive}"
    with Key.current_user(r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run").open(
        write=True
    ) as key:
        key[name] = cmd


def deregister_subst_drive(drive):
    """Deregister a subst drive in the registry"""
    name = f"paxo-subst-{drive}"
    with Key.current_user(r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run").open(
        write=True
    ) as key:
        del key[name]


def get_registered_subst_drives():
    """Get a list of registered subst drives"""
    result = {}
    with Key.current_user(
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
    ).open() as key:
        for name, value in key.items():
            if name.startswith("paxo-subst-"):
                value = shlex.split(value)
                result[name[11:]] = value[2]
    return result


def subst_drive_check(drive):
    """Check if drive is a subst drive"""
    drive = drive or work_drive_get()
    drive = validate_drivename(drive, check_exists=False)

    # if drive does not exist, we are ok
    if not os.path.isdir(drive):
        return True

    # if drive exists, we need to check if it is a subst drive
    target = is_subst(drive)
    if not target:
        raise click.ClickException(
            f"Intended work drive {drive} exists, but is not a work drive.  Please run 'paxo work activate --drive' to select another."
        )

    # look for the .paxo file
    if not os.path.isfile(os.path.join(drive, ".paxo")):
        raise click.ClickException(
            f"Intended work drive {drive} exists, but is not a paxo work drive.  Please run 'paxo work activate --drive' to select another."
        )

    return True


def work_drive_get():
    drive = env_var_get("PD_WORK_DRIVE")
    drive = drive or env_var_get("PD_SUBST_DRIVE")  # backwards compatibility
    if not drive:
        drive = config.work_drive_name
        work_drive_set(drive)
    return validate_drivename(drive, check_exists=False)


def work_drive_set(drive):
    drive = validate_drivename(drive, check_exists=False)
    subst_drive_check(drive)
    env_var_set("PD_WORK_DRIVE", drive)
    env_var_del("PD_SUBST_DRIVE")


def is_subst(drive):
    """Check if drive is a subst drive"""
    drive = validate_drivename(drive, check_exists=False)
    out = subprocess.run(["subst"], capture_output=True)
    for line in out.stdout.decode().splitlines():
        if line.startswith(drive):
            # return the part on the right side of the subst
            return line.split("=>")[1].strip()


def click_main(command, **extra_args):
    """run a click executable with an optional exception handler for no-console"""
    # do an initial check for --gui flags here because they have not been parsed yet
    if "--gui" in sys.argv[1:]:
        gui = True
    elif "--no-gui" not in sys.argv[1:]:
        gui = False
    else:
        gui = sys.executable.endswith("pythonw.exe")
    if gui:
        try:
            return command.main(standalone_mode=False, **extra_args)
        except click.Abort:
            tkinter.messagebox.showinfo("Aborted", "Operation aborted.")
            sys.exit(1)
        except click.ClickException as e:
            tkinter.messagebox.showerror("Error", e.format_message())
            sys.exit(e.exit_code)
        except Exception as e:
            tkinter.messagebox.showerror("Error", str(e))
            raise
    else:
        return command(**extra_args)


def query_long_filenames() -> bool:
    """Query if long filenames are enabled on the system"""
    with Key.local_machine(r"SYSTEM\CurrentControlSet\Control\FileSystem") as key:
        return key.get("LongPathsEnabled", 0) == 1


def enable_long_filenames(enable: bool) -> None:
    """Enable or disable long filenames on the system"""
    # enable long filenames
    with Key.local_machine(
        r"SYSTEM\CurrentControlSet\Control\FileSystem", write=True
    ) as key:
        key["LongPathsEnabled"] = 1 if enable else 0

    cmd = ["fsutil", "behavior", "set", "disable8dot3", "1" if enable else "0"]
    subprocess.check_call(cmd)


def get_invocation():
    script = sys.argv[0].lower()
    if script.endswith(".py"):
        # we are runing as executable plus script
        return sys.executable, [sys.argv[0]], sys.argv[1:]
    else:
        # we are running as a magic executable.
        return sys.argv[0], [], sys.argv[1:]


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


def elevate(reason: str = "", args: Optional[list[str]] = None):
    if not is_admin():
        # Re-run the program with admin rights
        if reason:
            click.echo(f"Requesting admin rights: {reason}")
        exe, first, rest = get_invocation()
        # replace the args with any new provided args
        if args is not None:
            rest = args
        r = ctypes.windll.shell32.ShellExecuteW(
            None, "runas", exe, " ".join(first + rest), None, 1
        )
        if r <= 32:
            raise RuntimeError("Failed to elevate to admin rights")
