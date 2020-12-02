from copy import deepcopy
import numpy as np

default_unit = 'a.u'


class Data(object):
    params = ['name', 'value', 'unit', 'metadata'],

    def __init__(self, name, value, unit=None, metadata={}, label_fmt=None, *args,
                 **kwargs):
        self.name = str(name)
        self.value = np.array(value)
        if unit is None or unit == '':
            unit = default_unit
        self.unit = str(unit)
        if label_fmt is None:
            label_fmt = lambda name, unit: f'{name} ({unit})'
        self.label_fmt = label_fmt
        self.metadata = metadata

    def parameters(self):
        dict_ = {}
        for param in self.params:
            value = getattr(self, param)
            dict_[param] = value
        dict_ = deepcopy(dict_)
        return dict_

    @property
    def label(self):
        return self.label_fmt(self.name, self.unit)

    def __repr__(self):
        cname = self.__class__.__name__
        out = f'{cname} - {str(self)}'
        return out

    def __str__(self):
        return f'name: {self.name}'


class Variable(Data):
    params = ['name', 'value', 'unit', 'metadata']

    def __init__(self, name, value, unit=None, metadata={}, **kwargs):
        super().__init__(name, value, unit, metadata, **kwargs)

    def get_value(self):
        value = deepcopy(self.value)
        return value

    def __str__(self):
        return f'name: {self.name} - unit: {self.unit} - shape: {self.value.shape}'


class Coord(Data):
    params = ['name', 'value', 'unit', 'offset', 'dim', 'metadata']

    def __init__(self, name, value, dim, unit=None, offset=0, metadata={}, **kwargs):
        super().__init__(name, value, unit, metadata, **kwargs)
        self.dim = int(dim)
        self.offset = np.array(offset)
        self.valueo = self.get_value(use_offset=True)

    def get_value(self, use_offset=False):
        value = deepcopy(self.value)
        if use_offset:
            value += self.offset
        return value

    def __str__(self):
        return f'name: {self.name} - unit: {self.unit} - shape: {self.value.shape} - dim: {self.dim}'


class InputVariable(Data):
    params = ['name', 'value', 'unit', 'comment', 'metadata']
    var_char = ''
    com_char = ''

    def __init__(self, name, value, unit='', comment='', metadata={}, **kwargs):
        super().__init__(name, value, unit, metadata, **kwargs)
        self.comment = comment

    def get_value(self):
        value = deepcopy(self.value)
        return value

    @property
    def text(self):
        t = f'{self.var_char}{self.name} = {self.value}'
        if self.comment:
            t = f'{t} {self.com_char} {self.comment}'
        return t

    def __str__(self):
        return self.text
