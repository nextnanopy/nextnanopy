from importlib.metadata import PackageNotFoundError, version

from nextnanopy.defaults import NNConfig, get_config
from nextnanopy.inputs import InputFile, Sweep
from nextnanopy.outputs import DataFile, DataFolder

try:
    __version__ = version("nextnanopy")
except PackageNotFoundError:
    # Package is not installed (e.g. running from a source checkout without
    # `pip install -e .`); there is no metadata to read the version from.
    __version__ = "unknown"

__all__ = [
    "NNConfig",
    "InputFile",
    "Sweep",
    "DataFile",
    "DataFolder",
    "config",
    "get_config",
    "__version__",
]


def __getattr__(name):
    # PEP 562: only called for names not already in the module namespace, i.e. for
    # `config` on its first access. Afterwards it still routes here, but get_config()
    # returns the cached object, so `nextnanopy.config` is the same instance every
    # time and `config.set(...)` followed by `config.save()` behaves as before.
    if name == "config":
        return get_config()
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
