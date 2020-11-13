import configparser
from copy import deepcopy
import os


def str_to_bool(string,
                true_cases=['true', 't', 'yes', 'y', '1'],
                false_cases=['false', 'f', 'no', 'n', '0'],
                ):
    str_low = string.lower()
    if str_low in true_cases:
        value = True
    elif str_low in false_cases:
        value = False
    else:
        raise ValueError('Ambiguos string to be converted to boolean')
    return value


def str_to_path(string):
    path = r'{}'.format(string)
    return path


class Config(object):
    def __init__(self, fullpath, validators={}):
        self.configparser = configparser.ConfigParser()
        self.validators = validators
        if fullpath:
            self.fullpath = fullpath
            self.load()

    def load(self):
        self.read_file()
        self.configparser_to_config()
        self.validate_config()

    def read_file(self):
        self.configparser.read(self.fullpath)

    def configparser_to_config(self):
        self.config = deepcopy(self.configparser._sections)

    def validate_config(self):
        for section in self.sections:
            if section not in self.validators.keys():
                continue
            for option, value in self.config[section].items():
                if option not in self.validators[section].keys():
                    continue
                validated_value = self.validators[section][option](value)
                self.config[section][option] = validated_value

    @property
    def sections(self):
        return self.config.keys()

    @property
    def preview(self):
        for sec in self.sections:
            print('[%s]' % (sec))
            for key, value in self.config[sec].items():
                print('{} = {}'.format(key, value))
            print('')

    def get_options(self, section):
        options = self.config[section]
        return options

    def save(self, fullpath=''):
        self.config_to_configparser()
        if not fullpath:
            fullpath = self.fullpath
        else:
            self.fullpath = fullpath
        with open(self.fullpath, 'w') as file:
            self.configparser.write(file)

    def config_to_configparser(self):
        for sec in self.sections:
            for key, value in self.config[sec].items():
                self.configparser[sec][key] = str(value)

    def set(self, section, option, value):
        if section in self.validators.keys():
            if option in self.validators[section].keys():
                value = self.validators[section][option](value)
        self.config[section][option] = value

    def get(self, section, option):
        return self.config[section][option]

    def add_section(self, section):
        if section not in self.sections:
            self.config[section] = {}
            self.configparser.add_section(section)

    def __repr__(self):
        lines = []
        lines.append(f'{self.__class__.__name__}({self.fullpath})')
        for sec in self.sections:
            lines.append(f'[{sec}]')
            for key, value in self.config[sec].items():
                lines.append(f'{key} = {value}')
        out = '\n'.join(lines)
        return out

    def __str__(self):
        return self.__repr__()


class NNConfig(Config):
    def __init__(self, fullpath=''):
        default_fullpath = os.path.join(os.environ['HOMEDRIVE'], os.environ['HOMEPATH'], '.nextnanopy-config')
        validators = {}
        validators['nextnano++'] = {
            'exe': str_to_path,
            'license': str_to_path,
            'database': str_to_path,
            'outputdirectory': str_to_path,
            'threads': int,
        }
        validators['nextnano3'] = {
            'exe': str_to_path,
            'license': str_to_path,
            'database': str_to_path,
            'threads': int,
            'outputdirectory': str_to_path,
            'debuglevel': int,
            'cancel': int,
            'softkill': int,
        }
        validators['nextnano.NEGF'] = {
            'exe': str_to_path,
            'license': str_to_path,
            'database': str_to_path,
            'outputdirectory': str_to_path,
            'threads': int,
        }

        self.default = {}
        self.default['nextnano++'] = {
            'exe': '',
            'license': '',
            'database': '',
            'outputdirectory': '',
            'threads': 0,
        }
        self.default['nextnano3'] = {
            'exe': '',
            'license': '',
            'database': '',
            'threads': 0,
            'outputdirectory': '',
            'debuglevel': 0,
            'cancel': -1,
            'softkill': -1,
        }
        self.default['nextnano.NEGF'] = {
            'exe': '',
            'license': '',
            'database': '',
            'outputdirectory': '',
            'threads': 0,
        }
        if not fullpath:
            fullpath = default_fullpath
        super().__init__(fullpath, validators)
        if not os.path.isfile(fullpath):
            self.to_default()
            self.save()

    def to_default(self):
        for section in self.default.keys():
            if section not in self.sections:
                self.add_section(section)
            for option, value in self.default[section].items():
                self.set(section, option, value)