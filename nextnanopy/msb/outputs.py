import numpy as np
from nextnanopy.utils.mycollections import DictList
from nextnanopy.outputs import Output, AvsAscii, Vtk, DataFileTemplate, Dat
from nextnanopy.utils.datasets import Variable, Coord
import re


class DataFile(DataFileTemplate):
    def __init__(self, fullpath, **loader_kwargs):
        super().__init__(fullpath, product="nextnano.MSB")
        self.load()

    def get_loader(self):
        if self.extension in [".v", ".fld", ".coord"]:
            loader = AvsAscii
        elif self.extension == ".vtr":
            loader = Vtk
        elif self.extension == ".txt":
            raise NotImplementedError(
                f"Loading nextnano.MSB datafiles with extension.txt is not implemented yet"
            )
        elif self.extension == ".dat":
            loader = Dat
        else:
            raise NotImplementedError(
                f"Loading datafile with extension {self.extension} is not implemented yet"
            )
        return loader
