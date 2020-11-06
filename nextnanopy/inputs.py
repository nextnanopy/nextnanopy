from nextnanopy.utils.formatting import text_to_lines, lines_to_text, input_file_type
from nextnanopy.utils.formatting import is_nn3_variable, is_nnp_variable
from nextnanopy.utils.formatting import parse_nn3_variable, parse_nnp_variable

from nextnanopy.utils.mycollections import DictList
from nextnanopy.utils.misc import savetxt
from nextnanopy.utils.datasets import InputVariable_nnp, InputVariable_nn3
from nextnanopy.utils.config import NNConfig
from .commands import execute as cmd_execute


class InputFile(object):
    def __init__(self, fullpath=None, configpath=None):
        self.raw_lines = []
        self.variables = DictList()
        self.type = 'not valid'
        if fullpath:
            self.load(fullpath)
        if not configpath:
            self.config = NNConfig()
        else:
            self.config = NNConfig(configpath)

    @property
    def text(self):
        return str(lines_to_text(*self.lines))

    @property
    def lines(self):
        new_lines = list(self.raw_lines)
        for ivar in self.variables.values():
            text = ivar.text
            idx = ivar.metadata['line_idx']
            new_lines[idx] = text
        return new_lines

    @property
    def preview(self, nums=True):
        for i, line in enumerate(self.lines):
            if nums:
                print(f'{i} {line}')
            else:
                print(f'{line}')

    @property
    def default_command_args(self):
        return self.config.config[self.type]

    @property
    def configpath(self):
        return self.config.fullpath

    def find_type(self):
        self.type = input_file_type(self.fullpath)
        return self.type

    def validate(self):
        if self.type not in ['nextnano++', 'nextnano3']:
            raise ValueError(f'Not valid input file')

    def load(self, fullpath):
        self.clear()
        self.fullpath = fullpath
        self.find_type()
        self.validate()
        self.load_raw()
        self.load_variables()

    def save(self, fullpath='', overwrite=False, automkdir=True):
        if fullpath:
            fullpath = self.fullpath
        self.fullpath = savetxt(fullpath=fullpath, text=self.text, overwrite=overwrite, automkdir=automkdir)
        return self.fullpath

    def execute(self, **kwargs):
        cmd_kwargs = dict(self.default_command_args)
        cmd_kwargs.update(kwargs)
        cmd_kwargs['inputfile'] = self.fullpath
        process = cmd_execute(**cmd_kwargs)
        return process

    def clear(self):
        self.raw_lines = []
        self.variables = DictList()
        self.fullpath = None

    def load_raw(self):
        with open(self.fullpath, 'r') as f:
            text = f.read()
        self.raw_lines = list(text_to_lines(text))
        return self.raw_lines

    def load_variables(self):
        variables = DictList()
        for i, line in enumerate(self.raw_lines):
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
        return self.variables

    def set_variable(self, name, value=None, comment=''):
        if name not in self.variables.keys():
            raise KeyError(f'{name} is not a valid variable.')
        if value:
            self.variables[name].value = value
        if comment:
            self.variables[name].comment = comment
        return self.variables[name]

