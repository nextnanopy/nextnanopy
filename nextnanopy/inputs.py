from nextnanopy.utils.formatting import text_to_lines, lines_to_text
from nextnanopy.utils.mycollections import DictList
from nextnanopy.utils.misc import savetxt
from nextnanopy.commands import execute as cmd_execute
from nextnanopy import defaults


class InputFileTemplate(object):
    def __init__(self, fullpath=None, configpath=None):
        self.raw_lines = []
        self.variables = DictList()
        self.fullpath = fullpath
        self.product = 'not valid'
        if fullpath is not None:
            self.load(fullpath)
        if configpath is None:
            self.config = defaults.NNConfig()
        else:
            self.config = defaults.NNConfig(configpath)

    @property
    def text(self):
        return str(lines_to_text(*self.lines))

    @text.setter
    def text(self, text):
        self.raw_lines = list(text_to_lines(text))
        self.find_product()
        self.validate()
        self.load_variables()

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
        return self.config.config[self.product]

    @property
    def configpath(self):
        return self.config.fullpath

    def load(self, fullpath):
        self.clear()
        self.fullpath = fullpath
        self.load_raw()
        self.find_product()
        self.validate()
        self.load_variables()

    def find_product(self):
        self.product = defaults.input_text_type(self.text)
        return self.product

    def validate(self):
        if self.product not in defaults.products:
            raise ValueError(f'Not valid input file')

    def save(self, fullpath=None, overwrite=False, automkdir=True):
        if fullpath is None:
            if self.fullpath is None:
                raise ValueError('Please, specify a fullpath')
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
        pass

    def get_variable(self, name):
        if name not in self.variables.keys():
            raise KeyError(f'{name} is not a valid variable.')
        return self.variables[name]

    def set_variable(self, name, value=None, comment=None):
        var = self.get_variable(name)
        if value is not None:
            var.value = value
        if comment is not None:
            var.comment = comment
        return var


class InputFile(InputFileTemplate):

    def load_variables(self):
        _InputFile = defaults.get_InputFile(self.product)
        file = _InputFile()
        file.text = self.text
        self.variables = file.variables
