# some features of the ue paths thing
from . import platform

_engine_root: str = "C:/Program Files/Epic Games/UE_4.27/Engine/"
_project_root: str = "C:/Users/username/Documents/Unreal Projects/MyProject/"


def set_engine_root(path: str):
    """Set the engine root path."""
    global _engine_root
    _engine_root = path
    if not _engine_root.endswith("/"):
        _engine_root += "/"
    platform.reset()


def set_project_root(path: str):
    """Set the project root path."""
    global _project_root
    _project_root = path
    if not _project_root.endswith("/"):
        _project_root += "/"
    platform.reset()


def engine_dir() -> str:
    """We are not an engine.  Just return a wonko string."""
    return _engine_root + "Engine/"


def project_dir() -> str:
    """We are not a project.  Just return a wonko string."""
    return _project_root


def engine_config_dir():
    return engine_dir() + "Config/"


def project_config_dir():
    return project_dir() + "Config/"


def engine_patform_extensions_dir() -> str:
    return engine_dir() + "Platforms/"


def project_patform_extensions_dir() -> str:
    return project_dir() + "Platforms/"
