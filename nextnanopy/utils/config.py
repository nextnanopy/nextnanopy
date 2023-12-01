import configparser
from copy import deepcopy


class Config(object):
    """
        This class stores and manipulates a configuration file.

        The initialization of the class will execute the load method.

        ...

        Parameters
        ----------
        fullpath : str
            path to the file.
        validators : dict
            dict where the keys are the name of the sections and the values
            are another dict.
            In the latter dict, the keys are the name of the options and the values
            are methods to convert the raw information (e.g: int)

        Attributes
        ----------

        fullpath : str
            path to the file
        config : dict
            validated values of each option of each section
        configparser : configparser.ConfigParser object
            ConfigParser object with raw values (str format) of each option of each section
        validators : dict
            dict of validator methods for each section and option (default is {})
        sections : list
            list of the section names

        Methods
        -------
        preview()
            print the text of the file.

        load()
            load the file located at .fullpath

        save(fullpath=None)
            save the current configuration into a file. (default is None)
            If it is None, it will use the current .fullpath

        get_options(section)
            get the list of option names of a given section

        config_to_configparser()
            copy the information in .config to .configparser

        set(section, option, value)
            change the value of a given option of a section in .config
            it applies the validator if there is any

        get(section, option)
            return the value of a given option of a section in .config

        add_section(section)
            create a new section in the configuration

    """
    def __init__(self, fullpath, validators=None):
        if validators is None:
            validators = {}
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

    def preview(self):
        for sec in self.sections:
            print('[%s]' % (sec))
            for key, value in self.config[sec].items():
                print('{} = {}'.format(key, value))
            print('')

    def get_options(self, section):
        options = self.config[section]
        return options

    def save(self, fullpath=None):
        self.config_to_configparser()
        if fullpath is None:
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
