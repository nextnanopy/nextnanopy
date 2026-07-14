from nextnanopy.outputs import DataFile as _DataFile
from nextnanopy.outputs import resolve_loader


def get_loader(extension, filename_only):
    return resolve_loader(extension, filename_only, product="nextnano.MSB")


class DataFile(_DataFile):
    """Backwards-compatible alias for nextnanopy.DataFile(..., product='nextnano.MSB')."""

    def __init__(self, fullpath, **loader_kwargs):
        super().__init__(fullpath, product="nextnano.MSB", **loader_kwargs)
