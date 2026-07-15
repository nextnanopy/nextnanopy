from importlib.metadata import PackageNotFoundError, version

from nextnanopy.commands import execute
from nextnanopy.defaults import NNConfig
from nextnanopy.inputs import InputFile, Sweep
from nextnanopy.outputs import DataFile, DataFolder

# from nextnanopy.shapes import GdsPolygonsRaw

try:
    __version__ = version("nextnanopy")
except PackageNotFoundError:
    # Package is not installed (e.g. running from a source checkout without
    # `pip install -e .`); there is no metadata to read the version from.
    __version__ = "unknown"

__all__ = [
    "execute",
    "NNConfig",
    "InputFile",
    "Sweep",
    "DataFile",
    "DataFolder",
    "config",
    "get_config",
    "__version__",
]

_config = None


def get_config():
    """Return the process-wide NNConfig, building it on first use.

    Constructing an NNConfig reads ~/.nextnanopy-config, and creates it if it is
    missing, so it is deliberately not done at import time: importing the package
    must not touch the user's home directory. `nextnanopy.config` resolves here via
    the module __getattr__ below, so the config is built on first access instead.
    """
    global _config
    if _config is None:
        _config = NNConfig()
    return _config


def __getattr__(name):
    # PEP 562: only called for names not already in the module namespace, i.e. for
    # `config` on its first access. Afterwards it still routes here, but get_config()
    # returns the cached object, so `nextnanopy.config` is the same instance every
    # time and `config.set(...)` followed by `config.save()` behaves as before.
    if name == "config":
        return get_config()
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
