import numpy as np
from nextnanopy.utils.mycollections import DictList
from nextnanopy.outputs import Output, AvsAscii, Vtk, DataFileTemplate
from nextnanopy.utils.datasets import Variable, Coord
import re
import os


class DataFile(DataFileTemplate):
    def __init__(self, fullpath, **loader_kwargs):
        super().__init__(fullpath, product='nextnano.NEGF')
        self.load(**loader_kwargs)

    def get_loader(self):
        if self.extension in ['.v', '.fld', '.coord']:
            loader = AvsAscii
        elif self.extension == '.vtr':
            loader = Vtk
        elif self.extension == '.txt':
            raise NotImplementedError(f'Loading nextnano.NEGF datafiles with extension.txt is not implemented yet')
        elif self.extension == '.dat':
            loader = Dat
        else:
            raise NotImplementedError(f'Loading datafile with extension {self.extension} is not implemented yet')
        return loader


class Dat(Output):
    def __init__(self, fullpath, **loader_kwargs):
        super().__init__(fullpath)
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

    def _get_nb_columns(self):
        meta = self.metadata
        with open(self.fullpath, 'r') as f:
            for i, line in enumerate(f):
                if i < meta['skip_rows']:
                    continue
                line = line.replace('\n', '').strip().split()
                arr = np.array(line)
                break
        return arr.size

    def load_metadata(self, FirstVarIsCoordFlag = True):
        headers = self._get_headers()
        self.metadata['headers'] = headers
        self.metadata['skip_rows'] = len(headers)
        nb = self._get_nb_columns()
        self.metadata['nb_columns'] = nb

        if len(headers) == 0:
            raise NotImplementedError('.dat file without header')
        else:
            header = headers[-1]  # take the last one by default
        header = re.split(r'\[|\]', header)
        header = [hi.strip() for hi in header]
        columns, units = header[0::2], header[1::2]
        diff = len(columns) - len(units)
        if len(columns) > nb:
            columns = columns[0:nb]
        elif diff > 0:
            empty = [''] * diff
            units.extend(empty)
        ndim = 0
        dkeys = []
        # FirstVarIsCoordFlag = True
        for i, (column, unit) in enumerate(zip(columns, units)):
            self.metadata[i] = {'name': column, 'unit': unit}
            if FirstVarIsCoordFlag:
                ndim += 1
                dkeys.append(i)
                FirstVarIsCoordFlag = False
        self.metadata['ndim'] = ndim
        self.metadata['dkeys'] = dkeys
        return self.metadata

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

def get_iv(path = ''):
    piv = os.path.join(path,'Current_vs_Voltage.dat')
    return np.loadtxt(piv,skiprows=1,delimiter='\t',unpack=True)

def get_WannierStark_on(folder):
    ws = np.loadtxt(folder + r'\WannierStark\\WannierStark_statesOn.dat',skiprows=2,delimiter='\t',unpack=True)
 #  print('Number of states: ', len(ws)-2)
    return ws

def get_WannierStark(folder):
    ws = np.loadtxt(folder + r'\WannierStark\\WannierStark_states.dat',skiprows=2,delimiter='\t',unpack=True)
 #  print('Number of states: ', len(ws)-2)
    return ws

def get_WannierStark_norm(folder,scaling_factor = 1):
    ws = np.loadtxt(folder + r'\WannierStark\\WannierStark_states.dat',skiprows=2,delimiter='\t',unpack=True)
 #  print('Number of states: ', len(ws)-2)
    norm = min(ws[1])
    z = ws[0]
    pot = ws[1]-norm
    ws_norm = ws[2:]-norm
    ws_norm_scal = scale_wf(ws_norm,scaling_factor)
    return z, pot, ws_norm_scal

def scale_wf(wf_input,factor):
    scaled = np.copy(wf_input)
    for i, cur  in enumerate(wf_input):
        mi = min(cur)
        ma = max(cur)
        scaled[i] = np.interp(cur,[mi,ma],[mi,factor*(ma-mi)+mi])
        
    return scaled
