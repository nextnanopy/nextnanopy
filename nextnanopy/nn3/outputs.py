import numpy as np
from nextnanopy.utils.mycollections import DictList
from nextnanopy.outputs import Output, AvsAscii, Vtk, DataFileTemplate
from nextnanopy.nn3.defaults import parse_nn3_variable, is_nn3_variable, InputVariable_nn3
from nextnanopy.utils.datasets import Variable, Coord
from nextnanopy.utils.formatting import best_str_to_name_unit


class DataFile(DataFileTemplate):
    def __init__(self, fullpath, **loader_kwargs):
        super().__init__(fullpath, product='nextnano3')
        self.load(**loader_kwargs)

    def get_loader(self):
        if self.extension in ['.v', '.fld', '.coord']:
            loader = AvsAscii
        elif self.extension == '.vtr':
            loader = Vtk
        elif self.extension == '.txt':
            loader = self._find_txt_loader()
        elif self.extension == '.dat':
            loader = Dat
        else:
            raise NotImplementedError(f'Loading datafile with extension {self.extension} is not implemented yet')
        return loader

    def _find_txt_loader(self):
        if self.filename_only in ['variables_input', 'variables_database']:
            loader = InputVariables
        elif self.filename_only == 'materials':
            NotImplementedError(f'Loading materials.txt is not implemented yet')
        elif self.filename_only == 'total_charges':
            NotImplementedError(f'Loading total_charges.txt is not implemented yet')
        else:
            raise NotImplementedError(f'Datafile {self.filename_only}.txt is not valid')
        return loader


class InputVariables(Output):
    def __init__(self, fullpath):
        super().__init__(fullpath)
        self.load()

    def load(self):
        self.load_raw()
        self.load_variables()

    def load_raw(self):
        with open(self.fullpath, 'r') as f:
            self.raw_lines = f.readlines()

    def load_variables(self):
        variables = DictList()
        for i, line in enumerate(self.raw_lines):
            if not is_nn3_variable(line):
                continue
            name, value, comment = parse_nn3_variable(line)
            var = InputVariable_nn3(name=name, value=value, comment=comment, metadata={'line_idx': i})
            variables[var.name] = var
        self.variables = variables
        return self.variables


class Dat(Output):
    def __init__(self, fullpath, **loader_kwargs):
        super().__init__(fullpath, product='nextnano3')
        self.load(**loader_kwargs)

    def load(self, **loader_kwargs):
        self.load_metadata(**loader_kwargs)
        self.load_data()

    def _get_headers(self):
        headers = []
        with open(self.fullpath, 'r') as f:
            for line in f:
                try:
                    float(line.split()[0])
                    break
                except:
                    headers.append(line)
        return headers

    def load_metadata(self, FirstVarIsCoordFlag = True):
        metadata = {}
        headers = self._get_headers()
        metadata['headers'] = headers
        metadata['skip_rows'] = len(headers)

        if len(headers) == 0:
            raise NotImplementedError('.dat file without header')
        else:
            header = headers[-1]  # take the last one by default
        header = header.split()
        ndim = 0
        dkeys = []
        # FirstVarIsCoordFlag = True
        for i, column in enumerate(header):
            key, unit = best_str_to_name_unit(column, default_unit=None)
            metadata[i] = {'name': key, 'unit': unit}
            # if key.lower() in ['x', 'y', 'z', 'position']:
            #    ndim += 1
            #    dkeys.append(i)
            if FirstVarIsCoordFlag:
                ndim += 1
                dkeys.append(i)
                FirstVarIsCoordFlag = False #use this to change behaviour of recognition of coords and variables

        metadata['ndim'] = ndim
        metadata['dkeys'] = dkeys
        self.metadata.update(metadata)
        return metadata

    def load_data(self):
        data = []
        meta = self.metadata
        with open(self.fullpath, 'r') as f:
            for i, line in enumerate(f):
                if i < meta['skip_rows']:
                    continue
                line = line.replace('\n', '').strip().split()
                if line:
                    data.append(line)
        data = np.array(data, dtype=float).T  # columns 1st index
        coords, variables = DictList(), DictList()
        dims = []
        for i, values in enumerate(data):
            vm = meta[i]
            if i in meta['dkeys']:
                #values = np.unique(values)
                dims.append(values.size)
                var = Coord(name=vm['name'], unit=vm['unit'], dim=i, value=values)
                coords[var.name] = var
            else:
                if dims:
                    values = values.reshape(*dims)
                var = Variable(name=vm['name'], unit=vm['unit'], value=values)
                variables[var.name] = var
        self.coords = coords
        self.variables = variables
        return coords, variables
