import os
from pathlib import Path
from nextnanopy.utils.config import Config

products = ['nextnano++', 'nextnano3', 'nextnano.NEGF', 'nextnano.MSB']
default_folder = str(Path.home())
config_default_path = os.path.join(default_folder, '.nextnanopy-config')
messages = {
    'load_input': [None, None],
    'save_input': [None, None],
    'execute_input': [None, None],
    'load_output': [None, None],
}


def get_InputFile(product):
    if product == 'nextnano++':
        from nextnanopy.nnp.inputs import InputFile
    elif product == 'nextnano3':
        from nextnanopy.nn3.inputs import InputFile
    elif product == 'nextnano.NEGF':
        from nextnanopy.negf.inputs import InputFile
    elif product == 'nextnano.MSB':
        from nextnanopy.msb.inputs import InputFile
    elif product == 'not valid':
        from nextnanopy.inputs import InputFileTemplate as InputFile
    else:
        raise ValueError(f'{product} is not valid')
    return InputFile


def get_DataFile(product):
    if product == 'nextnano3':
        from nextnanopy.nn3.outputs import DataFile
    elif product == 'nextnano++':
        from nextnanopy.nnp.outputs import DataFile
    elif product == 'nextnano.NEGF':
        from nextnanopy.negf.outputs import DataFile
    elif product == 'nextnano.MSB':
        from nextnanopy.negf.outputs import DataFile
    else:
        raise ValueError(f'{product} is not valid')
    return DataFile


def get_command(product):
    if product == 'nextnano++':
        from nextnanopy.nnp.defaults import command_nnp as command
    elif product == 'nextnano3':
        from nextnanopy.nn3.defaults import command_nn3 as command
    elif product == 'nextnano.NEGF':
        from nextnanopy.negf.defaults import command_negf as command
    elif product == 'nextnano.MSB':
        from nextnanopy.msb.defaults import command_msb as command
    else:
        raise ValueError(f'{product} is not valid')
    return command


def get_fmt(product):
    if product == 'nextnano++':
        from nextnanopy.nnp.defaults import fmt
    elif product == 'nextnano3':
        from nextnanopy.nn3.defaults import fmt
    elif product == 'nextnano.NEGF':
        from nextnanopy.negf.defaults import fmt
    elif product == 'nextnano.MSB':
        from nextnanopy.msb.defaults import fmt
    else:
        raise ValueError(f'{product} is not valid')
    return fmt


def input_file_type(fullpath):
    from nextnanopy.nnp.defaults import is_nnp_input_file
    from nextnanopy.nn3.defaults import is_nn3_input_file
    from nextnanopy.negf.defaults import is_negf_input_file
    from nextnanopy.msb.defaults import is_msb_input_file
    if is_nn3_input_file(fullpath):
        return 'nextnano3'
    elif is_nnp_input_file(fullpath):
        return 'nextnano++'
    elif is_negf_input_file(fullpath):
        return 'nextnano.NEGF'
    elif is_msb_input_file(fullpath):
        return 'nextnano.MSB'
    else:
        return 'not valid'


def input_text_type(text):
    from nextnanopy.nnp.defaults import is_nnp_input_text
    from nextnanopy.nn3.defaults import is_nn3_input_text
    from nextnanopy.negf.defaults import is_negf_input_text
    from nextnanopy.msb.defaults import is_msb_input_text
    if is_nn3_input_text(text):
        return 'nextnano3'
    elif is_nnp_input_text(text):
        return 'nextnano++'
    elif is_negf_input_text(text):
        return 'nextnano.NEGF'
    elif is_msb_input_text(text):
        return 'nextnano.MSB'
    else:
        return 'not valid'


def get_config_validators():
    config_validator = {product: _get_config_validator(product) for product in products}
    return config_validator


def get_config_defaults():
    config_defaults = {product: _get_config_default(product) for product in products}
    return config_defaults


def _get_config_validator(product):
    if product == 'nextnano++':
        from nextnanopy.nnp.defaults import config_validator
    elif product == 'nextnano3':
        from nextnanopy.nn3.defaults import config_validator
    elif product == 'nextnano.NEGF':
        from nextnanopy.negf.defaults import config_validator
    elif product == 'nextnano.MSB':
        from nextnanopy.msb.defaults import config_validator
    else:
        raise ValueError(f'{product} is not valid')
    return config_validator


def _get_config_default(product):
    if product == 'nextnano++':
        from nextnanopy.nnp.defaults import config_default
    elif product == 'nextnano3':
        from nextnanopy.nn3.defaults import config_default
    elif product == 'nextnano.NEGF':
        from nextnanopy.negf.defaults import config_default
    elif product == 'nextnano.MSB':
        from nextnanopy.msb.defaults import config_default
    else:
        raise ValueError(f'{product} is not valid')
    return config_default


class NNConfig(Config):
    def __init__(self, fullpath=None):
        self.default_fullpath = config_default_path
        validators = get_config_validators()
        self.defaults = get_config_defaults()
        if fullpath is None:
            fullpath = self.default_fullpath
        super().__init__(fullpath, validators)
        if not os.path.isfile(fullpath):
            self.to_default()
            self.save()

    def to_default(self):
        for section in self.defaults.keys():
            if section not in self.sections:
                self.add_section(section)
            for option, value in self.defaults[section].items():
                self.set(section, option, value)

    def reset(self):
        self.to_default()
        self.save()
