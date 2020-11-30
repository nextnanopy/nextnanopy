import os
from itertools import islice
import numpy as np

from nextnanopy.utils.datasets import Variable, Coord
from nextnanopy.utils.mycollections import DictList

from nextnanopy import defaults


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

    def get_coord(self, key):
        return self.coords[key]

    def get_variable(self, key):
        return self.variables[key]


class DataFileTemplate(Output):
    def __init__(self, fullpath, product=None):
        super().__init__(fullpath)
        self.product = product
        self.load()

    @load_message
    def load(self):
        loader = self.get_loader()
        df = loader(self.fullpath)
        self.update_with_datafile(df)
        del df

    def update_with_datafile(self, datafile):
        self.metadata.update(datafile.metadata)
        self.coords.update(datafile.coords)
        self.variables.update(datafile.variables)

    def get_loader(self):
        pass


class DataFile(DataFileTemplate):
    def __init__(self, fullpath, product=None):
        super().__init__(fullpath, product=product)

    def get_loader(self):
        if self.product:
            loader = defaults.get_DataFile(self.product)
        else:
            print('[Warning] nextnano product is not specified: nextnano++, nextnano3, nextnano.NEGF or nextnano.MSB')
            print('[Warning] Autosearching for the best loading method. Note: The result may not be correct')
            loader = self.find_loader()
        return loader

    def find_loader(self):
        from nextnanopy.nnp.outputs import DataFile as DataFile_nnp
        from nextnanopy.nn3.outputs import DataFile as DataFile_nn3
        from nextnanopy.negf.outputs import DataFile as DataFile_negf
        Dats = [DataFile_nn3, DataFile_nnp, DataFile_negf]
        for Dati in Dats:
            try:
                df = Dati(self.fullpath)
                if '' in df.variables.keys():
                    continue
                else:
                    break
            except:
                pass
        loader = Dati
        return loader


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


class VtrAscii(Output):
    def __init__(self, fullpath):
        super().__init__(fullpath)
        self.load()

    def load(self):
        x, y, z = load_vtr(self.fullpath)
        self.coords['x'] = Coord(name='x', value=x, unit=None, dim=0)
        self.coords['y'] = Coord(name='y', value=y, unit=None, dim=1)
        self.variables[''] = Variable(name='', value=z, unit='')


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
	
def load_vtr(path: str):
    """
    Loads VTR file. \n
    Returns X, Y, Z as numpy arrays.
    """
    fp = open(path,'r')
    lines = fp.readlines()

    beg = []
    end = []

    for i in range(len(lines)):
        cur_beg_ind = lines[i].find('<DataArray')
        if cur_beg_ind != -1:
            beg.append((i,cur_beg_ind))
    
        cur_end_ind = lines[i].find('</DataArray>')
        if cur_end_ind != -1:
            end.append((i,cur_end_ind))
            
    X=[]
    for i in range(beg[0][0]+1,end[0][0]+1):
        if i != end[0][0]:

            X_temp = lines[i].replace('\n','').split('\t') # Here, it seems a 'tab' separator is assumed to be present.
         #  X_temp = lines[i].replace('\n','').split(' ')
         #  print(f'X_temp = ',X_temp) 

            X_temp = list(map(float,X_temp))
          # X_temp = list(np.array(X_temp,dtype=np.float64)) # Birner test
            X = X + X_temp
            
        if i == end[0][0]:
            last = lines[i].split('\t')
            del last[-1]
            X = X + list(map(float,last))
            

            
    X = np.asarray(X)
    
    Y=[]
    for i in range(beg[1][0]+1,end[1][0]+1):
        if i != end[1][0]:
            Y_temp = lines[i].replace('\n','').split('\t')
            Y_temp = list(map(float,Y_temp))
            Y = Y + Y_temp
            
        if i == end[1][0]:
            last = lines[i].split('\t')
            del last[-1]
            Y = Y + list(map(float,last))
            

            
    Y = np.asarray(Y)
    
    Z=[]
    for i in range(beg[3][0]+1,end[3][0]+1):
        if i != end[3][0]:
            Z_temp = lines[i].replace('\n','').split('\t')
            Z_temp = list(map(float,Z_temp))
            Z = Z + Z_temp
            
        if i == end[3][0]:
            last = lines[i].split('\t')
            del last[-1]
            Z = Z + list(map(float,last))
            
    Z = np.asarray(Z)
    Z = np.reshape(Z,(len(Y),len(X)))
    
    return X, Y, Z
	
