from functools import partial

from nextnanopy.nnp.defaults import (
    InputVariable_nnp,
    is_nnp_variable,
    parse_nnp_variable,
)
from nextnanopy.outputs import Dat, Output, resolve_loader
from nextnanopy.outputs import DataFile as _DataFile
from nextnanopy.utils.datasets import Variable
from nextnanopy.utils.mycollections import DictList


def get_loader(extension, filename_only):
    return resolve_loader(extension, filename_only, txt_loader=_txt_loader, product="nextnano++")


def _txt_loader(filename_only):
    if filename_only in ["variables_input", "variables_database"]:
        loader = InputVariables
    elif filename_only == "materials":
        raise NotImplementedError("Loading materials.txt is not implemented yet")
    elif filename_only == "total_charges":
        loader = TotalCharges
    else:
        loader = partial(Dat, FirstVarIsCoordFlag=False)
    return loader


class DataFile(_DataFile):
    """Backwards-compatible alias for nextnanopy.DataFile(..., product='nextnano++')."""

    def __init__(self, fullpath, **loader_kwargs):
        super().__init__(fullpath, product="nextnano++", **loader_kwargs)


class InputVariables(Output):
    def __init__(self, fullpath, **loader_kwargs):
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
            if not is_nnp_variable(line):
                continue
            name, value, comment = parse_nnp_variable(line)
            var = InputVariable_nnp(
                name=name, value=value, comment=comment, metadata={"line_idx": i}
            )
            variables[var.name] = var
        self.variables = variables
        return self.variables


class TotalCharges(Output):
    def __init__(self, fullpath, **loader_kwargs):
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
            try:
                name, value, unit = line.split()
            except Exception as e:
                raise ValueError(
                    f"Malformed line {i + 1} in total_charges file {self.fullpath}: "
                    f"expected 'name value unit', got {line.strip()!r}"
                ) from e

            try:
                value = float(value)
            except Exception as e:
                raise ValueError(
                    f"Non-numeric value on line {i + 1} in total_charges file "
                    f"{self.fullpath}: {value!r}"
                ) from e

            # temp solution to omit ":" in the end of the line
            if name[-1] == ":":
                name = name[:-1]

            var = Variable(name=name, unit=unit, value=value)
            variables[var.name] = var

        self.variables = variables
        return self.variables


# class Dat(Output):
#     def __init__(self, fullpath, FirstVarIsCoordFlag=True):
#         super().__init__(fullpath)
#         self.load(FirstVarIsCoordFlag)

#     def load(self, FirstVarIsCoordFlag):
#         self.load_metadata(FirstVarIsCoordFlag)
#         self.load_data()

#     def _get_headers(self):
#         headers = []
#         with open(self.fullpath, "r") as f:
#             for line in f:
#                 try:
#                     float(line.split()[0])
#                     break
#                 except:
#                     headers.append(line)
#         return headers

#     def load_metadata(self, FirstVarIsCoordFlag):
#         metadata = {}
#         headers = self._get_headers()
#         metadata["headers"] = headers
#         metadata["skip_rows"] = len(headers)

#         if len(headers) == 0:
#             raise NotImplementedError(".dat file without header")
#         else:
#             header = headers[-1]  # take the last one by default
#         header = header.split()
#         ndim = 0
#         dkeys = []

#         # FirstVarIsCoordFlag = True
#         for i, column in enumerate(header):
#             key, unit = best_str_to_name_unit(column, default_unit=None)
#             metadata[i] = {"name": key, "unit": unit}
#             # if key.lower() in ['x', 'y', 'z', 'position']:
#             #    ndim += 1
#             #    dkeys.append(i)
#             if FirstVarIsCoordFlag:
#                 ndim += 1
#                 dkeys.append(i)
#                 FirstVarIsCoordFlag = False  # use this to change behaviour of recognition of coords and variables
#         metadata["ndim"] = ndim
#         metadata["dkeys"] = dkeys
#         self.metadata.update(metadata)
#         return metadata

#     def load_data(self):
#         data = []
#         meta = self.metadata
#         # with open(self.fullpath, 'r') as f:
#         #     for i, line in enumerate(f):
#         #         if i < meta['skip_rows']:
#         #             continue
#         #         line = line.replace('\n', '').strip().split()
#         #         if line:
#         #             data.append(line)
#         data = np.loadtxt(self.fullpath, skiprows=meta["skip_rows"])
#         data = np.array(data, dtype=float).T  # columns 1st index
#         coords, variables = DictList(), DictList()
#         dims = []
#         for i, values in enumerate(data):
#             vm = meta[i]
#             if i in meta["dkeys"]:
#                 # values = np.unique(values)
#                 dims.append(values.size)
#                 var = Coord(name=vm["name"], unit=vm["unit"], dim=i, value=values)
#                 coords[var.name] = var
#             else:
#                 if dims:
#                     values = values.reshape(*dims)
#                 var = Variable(name=vm["name"], unit=vm["unit"], value=values)
#                 variables[var.name] = var
#         self.coords = coords
#         self.variables = variables
#         return coords, variables

#     def save(self, new_location, extension="dat"):
#         with open(new_location, "w") as f:
#             # Write headers
#             for header in self.metadata["headers"]:
#                 f.write(header)

#             # Write data
#             combined_data = [coord.value for coord in self.coords] + [
#                 variable.value for variable in self.variables
#             ]

#             data = np.column_stack(combined_data).transpose()
#             np.savetxt(f, data.T)

#         # Optionally update the fullpath attribute to the new location
#         self.fullpath = new_location
