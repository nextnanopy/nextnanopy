import numpy as np
from nextnanopy.utils.mycollections import DictList
from nextnanopy.outputs import Output, AvsAscii, Vtk, DataFileTemplate, Dat
from nextnanopy.nn3.defaults import (
    parse_nn3_variable,
    is_nn3_variable,
    InputVariable_nn3,
)
from nextnanopy.utils.datasets import Variable, Coord
from nextnanopy.utils.formatting import best_str_to_name_unit


class DataFile(DataFileTemplate):
    def __init__(self, fullpath, **loader_kwargs):
        super().__init__(fullpath, product="nextnano3")
        self.load(**loader_kwargs)

    def get_loader(self):
        if self.extension in [".v", ".fld", ".coord"]:
            loader = AvsAscii
        elif self.extension == ".vtr":
            loader = Vtk
        elif self.extension == ".txt":
            loader = self._find_txt_loader()
        elif self.extension == ".dat":
            loader = Dat
        else:
            raise NotImplementedError(
                f"Loading datafile with extension {self.extension} is not implemented yet"
            )
        return loader

    def _find_txt_loader(self):
        if self.filename_only in ["variables_input", "variables_database"]:
            loader = InputVariables
        elif self.filename_only == "materials":
            NotImplementedError(f"Loading materials.txt is not implemented yet")
        elif self.filename_only == "total_charges":
            NotImplementedError(f"Loading total_charges.txt is not implemented yet")
        else:
            raise NotImplementedError(f"Datafile {self.filename_only}.txt is not valid")
        return loader


class InputVariables(Output):
    def __init__(self, fullpath):
        super().__init__(fullpath)
        self.load()

    def load(self):
        self.load_raw()
        self.load_variables()

    def load_raw(self):
        with open(self.fullpath, "r") as f:
            self.raw_lines = f.readlines()

    def load_variables(self):
        variables = DictList()
        for i, line in enumerate(self.raw_lines):
            if not is_nn3_variable(line):
                continue
            name, value, comment = parse_nn3_variable(line)
            var = InputVariable_nn3(
                name=name, value=value, comment=comment, metadata={"line_idx": i}
            )
            variables[var.name] = var
        self.variables = variables
        return self.variables
