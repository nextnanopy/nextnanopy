import os
from itertools import islice
import numpy as np

from .utils.datasets import Variable, Coord, InputVariable_nn3, InputVariable_nnp
from .utils.mycollections import DictList

from .utils.formatting import is_nn3_variable, is_nnp_variable
from .utils.formatting import parse_nn3_variable, parse_nnp_variable


def load_message(method):
    def f(*args, **kwargs):
        # print('Loading...')
        result = method(*args, **kwargs)
        # print('Done!')

    return f


class Output(object):
    def __init__(self, fullpath):
        self.fullpath = fullpath
        self.metadata = {}
        self.coords = DictList()
        self.variables = DictList()

    @property
    def folder(self):
        return os.path.split(self.fullpath)[0]

    @property
    def filename(self):
        name = os.path.split(self.fullpath)[-1]
        return os.path.splitext(name)[0]

    @property
    def extension(self):
        return os.path.splitext(self.fullpath)[-1]

    @load_message
    def load(self):
        pass


class Datafile(Output):
    def __init__(self, fullpath):
        super().__init__(fullpath)
        self.load()

    @load_message
    def load(self):
        loader = self.get_loader()
        df = loader(self.fullpath)
        self.update_with_datafile(df)
        del df

    def get_loader(self):
        if self.extension in ['.v', '.fld', '.coord']:
            loader = AvsAscii
        elif self.extension == '.txt':
            loader = self._find_txt_loader()
        elif self.extension == '.dat':
            loader = Dat
        else:
            raise ValueError(f'Loading datafile with extension {self.extension} is not implemented yet')
        return loader

    def _find_txt_loader(self):
        if self.filename in ['variables_input', 'variables_database']:
            loader = InputVariables
        elif self.filename == 'materials':
            NotImplementedError(f'Loading materials.txt is not implemented yet')
        elif self.filename == 'total_charges':
            NotImplementedError(f'Loading total_charges.txt is not implemented yet')
        else:
            raise ValueError(f'Datafile {self.filename}.txt is not valid')
        return loader

    def update_with_datafile(self, datafile):
        self.metadata.update(datafile.metadata)
        self.coords.update(datafile.coords)
        self.variables.update(datafile.variables)


class Dat(Output):
    def __init__(self, fullpath):
        super().__init__(fullpath)
        self.load()

    def load(self):
        self.load_metadata()
        self.load_data()

    def load_metadata(self):
        with open(self.fullpath, 'r') as f:
            header = f.readline().split()
        metadata = {}
        ndim = 0
        dkeys = []
        for i, column in enumerate(header):
            if '[' in column:
                key, unit = column.split('[')
                unit = unit.replace(']', '')
            else:
                key = column
                unit = ''
            metadata[i] = {'name': key, 'unit': unit}
            if key in ['x', 'y', 'z', 'position']:
                ndim += 1
                dkeys.append(i)
        metadata['ndim'] = ndim
        metadata['dkeys'] = dkeys
        self.metadata.update(metadata)
        return metadata

    def load_data(self):
        data = []
        meta = self.metadata
        with open(self.fullpath, 'r') as f:
            for i, line in enumerate(f):
                if i == 0:
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
                values = np.unique(values)
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


class InputVariables(Output):
    def __init__(self, fullpath):
        super().__init__(fullpath)
        self.load()

    def load(self):
        self.load_variables()

    def load_variables(self):
        variables = DictList()
        with open(self.fullpath, 'r') as f:
            for i, line in enumerate(f):
                if is_nnp_variable(line):
                    name, value, comment = parse_nnp_variable(line)
                    var = InputVariable_nnp(name=name, value=value, comment=comment, metadata={'line_idx': i})
                elif is_nn3_variable(line):
                    name, value, comment = parse_nn3_variable(line)
                    var = InputVariable_nn3(name=name, value=value, comment=comment, metadata={'line_idx': i})
                else:
                    continue
                variables[var.name] = var
            self.variables = variables
        return variables


class Variables(Output):
    def __init__(self, fullpath):
        super().__init__(fullpath)
        self.load()

    def load(self):
        self.load_variables()

    def load_variables(self):
        variables = DictList()
        with open(self.fullpath, 'r') as f:
            for line in f:
                line = line.split()
                if not line or line[0] == '#':
                    continue
                name = line[0].replace('$', '')
                value = line[-1].replace('\n', '')
                try:
                    value = float(value)
                except:
                    pass
                var = Variable(name=name, value=value)
                variables[var.name] = var
            self.variables = variables
        return variables


class AvsAscii(Output):
    def __init__(self, fullpath):
        super().__init__(fullpath)
        self.load()

    @property
    def fld(self):
        filename = self.filename + '.fld'
        return os.path.join(self.folder, filename)

    def load(self):
        self.load_raw_metadata()
        self.load_metadata()
        self.load_variables()
        self.load_coords()

    def load_raw_metadata(self):
        info = []
        with open(self.fld, 'r') as f:
            for line in f:
                line = line.replace('\n', '')
                line = line.strip()
                try:
                    float(line)
                    break
                except:
                    if line == '':
                        continue
                    if line[0] != '#':
                        info.append(line)
        return info

    def load_metadata(self):
        info = self.load_raw_metadata()
        key_int = ['ndim', 'dim1', 'dim2', 'dim3', 'nspace', 'veclen']
        key_str = ['data', 'field']
        metadata = {}
        metadata['labels'] = []
        metadata['units'] = []
        metadata['variables'] = []
        metadata['coords'] = []
        metadata['dims'] = []
        for line in info:
            key, value = line.split(maxsplit=1)
            if value[0] == '=':
                value = value.replace('=', '')
                value = value.strip()
                if key in key_int:
                    value = int(value)
                    metadata[key] = value
                elif key == 'label':
                    labels = value.split()
                    for label in labels:
                        if '[' in label:
                            label, unit = label.split('[')
                            unit = unit.split(']')[0]
                        else:
                            label = label
                            unit = ''
                        metadata['labels'].append(label)
                        metadata['units'].append(unit)
                else:
                    value = str(value)
                    metadata[key] = value

                if key[:3] == 'dim':
                    metadata['dims'].append(metadata[key])

            else:
                if key == 'variable':
                    vm = values_metadata(line)
                    vm['file'] = os.path.join(self.folder, vm['file'])
                    vm['size'] = np.prod(metadata['dims'])
                    metadata['variables'].append(vm)
                elif key == 'coord':
                    vm = values_metadata(line)
                    vm['file'] = os.path.join(self.folder, vm['file'])
                    num = vm['num']
                    vm['size'] = metadata[f'dim{num}']
                    metadata['coords'].append(vm)

        self.metadata = metadata
        return metadata

    def load_variables(self):
        meta = self.metadata
        variables = DictList()
        for vmeta, label, unit in zip(meta['variables'], meta['labels'], meta['units']):
            values = load_values(file=vmeta['file'],
                                 filetype=vmeta['filetype'],
                                 skip=vmeta['skip'],
                                 offset=vmeta['offset'],
                                 stride=vmeta['stride'],
                                 size=vmeta['size'])
            values = reshape_values(values, *meta['dims'])
            var = Variable(name=label, value=values, unit=unit, metadata=vmeta)
            variables[var.name] = var
        self.variables = variables
        return variables

    def load_coords(self):
        meta = self.metadata
        coords = DictList()
        for vmeta in meta['coords']:
            values = load_values(file=vmeta['file'],
                                 filetype=vmeta['filetype'],
                                 skip=vmeta['skip'],
                                 offset=vmeta['offset'],
                                 stride=vmeta['stride'],
                                 size=vmeta['size'])
            ax = coord_axis(vmeta['num'])
            unit = 'nm'
            var = Coord(name=ax, value=values, unit=unit, dim=vmeta['num'] - 1, metadata=vmeta)
            coords[var.name] = var
        self.coords = coords
        return coords


def coord_axis(dim):
    dim = str(dim)
    axes = {'1': 'x', '2': 'y', '3': 'z'}
    return axes[dim]


def values_metadata(line):
    """ Return a dict for: kind, num, file, filetype, skip, offset, stride"""
    metadata = {}
    kind, num, rest = line.split(maxsplit=2)
    metadata['kind'] = kind
    metadata['num'] = int(num)
    raw_rest = rest.split('=')
    raw_rest = [r.strip().split() for r in raw_rest]
    rest = []
    for ri in raw_rest:
        rest.extend(ri)
    keys = rest[0::2]
    values = rest[1::2]
    for key, value in zip(keys, values):
        key = key.strip()
        value = value.strip()
        if key in ['num', 'skip', 'offset', 'stride']:
            value = int(value)
        metadata[key] = value
    return metadata


def load_values(file, filetype='ascii', skip=0, offset=0, stride=1, size=None):
    """ Return flat array of floating values """
    stop = skip + size if size != None else None
    with open(file, 'r') as f:
        lines = islice(f, skip, stop, 1)
        values = [line.replace('\n', '').strip().split()[offset] for line in lines]
    return np.array(values, dtype=float)


def reshape_values(values, *dims):
    dims = np.flip(dims)
    shape = tuple([dim for dim in dims])
    values = np.reshape(values, shape)
    return np.transpose(values)
