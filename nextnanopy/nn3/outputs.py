from nextnanopy.nn3.defaults import (
    InputVariable_nn3,
    is_nn3_variable,
    parse_nn3_variable,
)
from nextnanopy.outputs import DataFile as _DataFile
from nextnanopy.outputs import Output, resolve_loader
from nextnanopy.utils.mycollections import DictList


def get_loader(extension, filename_only):
    return resolve_loader(extension, filename_only, txt_loader=_txt_loader, product="nextnano3")


def _txt_loader(filename_only):
    if filename_only in ["variables_input", "variables_database"]:
        loader = InputVariables
    elif filename_only == "materials":
        raise NotImplementedError("Loading materials.txt is not implemented yet")
    elif filename_only == "total_charges":
        raise NotImplementedError("Loading total_charges.txt is not implemented yet")
    else:
        raise NotImplementedError(f"Datafile {filename_only}.txt is not valid")
    return loader


class DataFile(_DataFile):
    """Backwards-compatible alias for nextnanopy.DataFile(..., product='nextnano3')."""

    def __init__(self, fullpath, **loader_kwargs):
        super().__init__(fullpath, product="nextnano3", **loader_kwargs)


class InputVariables(Output):
    def __init__(self, fullpath):
        super().__init__(fullpath)
        self.load()

    def load(self):
        self.load_raw()
        self.load_variables()

    def load_raw(self):
        with open(self.fullpath) as f:
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
