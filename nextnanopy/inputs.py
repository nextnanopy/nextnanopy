import os
import warnings
import itertools
from nextnanopy.utils.formatting import text_to_lines, lines_to_text
from nextnanopy.utils.mycollections import DictList
from nextnanopy.utils.misc import savetxt, get_filename, get_folder, get_file_extension, message_decorator, mkdir_even_if_exists, mkdir_if_not_exist
from nextnanopy.commands import execute as cmd_execute
from nextnanopy import defaults
from collections.abc import Iterable


_msgs = defaults.messages['load_input']
load_message = lambda method: message_decorator(method, init_msg=_msgs[0], end_msg=_msgs[1])
_msgs = defaults.messages['save_input']
save_message = lambda method: message_decorator(method, init_msg=_msgs[0], end_msg=_msgs[1])
_msgs = defaults.messages['execute_input']
execute_message = lambda method: message_decorator(method, init_msg=_msgs[0], end_msg=_msgs[1])


class InputFileTemplate(object):
    """
        This class stores and manipulates any kind of nextnano input files.
        For each nextnano product, the syntax is different but the core information
        is very similar like the variables that can be changed.
        This class contains useful methods such as to get a preview of the file or
        execute a simulation.

        The initialization of the class will execute the load method and setup the
        config file.

        ...

        Parameters
        ----------
        fullpath : str
            path to the file.
            If it is not None, it will load the file (default: None)
        configpath : str
            path to the config file.
            If it is None, it will use the default configuration (default: None)


        Attributes
        ----------

        fullpath : str
            path to the file (default: None)
        configpath : str
            path to the config file (default: your home path)
        variables : DictList
            input variables defined in the file (default: DictList())
        raw_lines : list
            list of str of each line in the file
        text : str
            raw text of the file (settable)
        lines : list
            raw_lines updated with the current input variable parameters
        filename : str
            name with the file extension (settable)
        filename_only :
            name without the file extension (settable)
        folder_input : str
            folder of the fullpath (settable)
        folder_output : str
            folder where the simulated data is stored after execution
        product : str
            detected nextnano product when the file is loaded (default: 'not valid')
        config: nextnano.NNConfig
            config file object
        execute_info: dict
            information after executing the file

        Methods
        -------
        preview(nums=True)
            print the text of the file.

        load(fullpath)
            load an input file

        save(fullpath=None, overwrite=False, automkdir=True)
            save the current information into a file.

        execute(**kwargs)
            execute the input file located at .fullpath

        get_variable(name)
            equivalent to self.variables[name]

        set_variable(name, value=None, comment=None)
            change the value and/or the comment of self.variable[name]
            If value or comment is None, it won't change that parameter
    """

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
        self.execute_info = {}

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
    def raw_text(self):
        return str(lines_to_text(*self.raw_lines))

    @property
    def lines(self):
        new_lines = list(self.raw_lines)
        for ivar in self.variables.values():
            text = ivar.text
            idx = ivar.metadata['line_idx']
            new_lines[idx] = text
        return new_lines

    @property
    def default_command_args(self):
        return self.config.config[self.product]

    @property
    def configpath(self):
        return self.config.fullpath

    @property
    def filename_only(self):
        return get_filename(self.fullpath, ext=False)

    @filename_only.setter
    def filename_only(self, name):
        ext = get_file_extension(self.fullpath)
        self.filename = f'{name}{ext}'

    @property
    def filename(self):
        return get_filename(self.fullpath, ext=True)

    @filename.setter
    def filename(self, name):
        self.fullpath = os.path.join(self.folder_input, name)

    @property
    def folder_input(self):
        return get_folder(self.fullpath)

    @folder_input.setter
    def folder_input(self, folder):
        self.fullpath = os.path.join(folder, self.filename)

    @property
    def folder_output(self):
        key = 'outputdirectory'
        if key in self.execute_info.keys():
            return self.execute_info[key]
        else:
            raise KeyError('Input file has not been executed yet')

    def preview(self, nums=True):
        """
        Print the text of the file.

        Parameters
        ----------
        nums : bool, optional
            If it is True, it will show the number of each line. (default is True)
        """
        for i, line in enumerate(self.lines):
            if nums:
                print(f'{i} {line}')
            else:
                print(f'{line}')

    @load_message
    def load(self, fullpath):
        """
        The steps are the following:
            1. clear the current information
            2. load the raw text (update .fullpath and .raw_lines)
            3. find the nextnano product (update .product)
            4. validate the input file
            5. load the input variables (update .variables)

        Parameters
        ----------
        fullpath : str
            path to the file to be loaded
        """
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

    @save_message
    def save(self, fullpath=None, overwrite=False, automkdir=True):
        """
        Save the current information into a file.

        Parameters
        ----------
        fullpath : str, optional
            path including the file name where it will be saved (default is None)
            If None, it will use the current .fullpath
        overwrite : bool, optional
            If it is False, it will find an unused name by adding an extra index like _1
            (default is False)
        automkdir : bool, optional
            If it is True, it will create the folder if it does not exist.
            (default is False)
        """
        if fullpath is None:
            if self.fullpath is None:
                raise ValueError('Please, specify a fullpath')
            fullpath = self.fullpath
        self.fullpath = savetxt(fullpath=fullpath, text=self.text, overwrite=overwrite, automkdir=automkdir)
        return self.fullpath

    @execute_message
    def execute(self, **kwargs):
        """
        Execute the input file located at .fullpath
        Individual kwargs can be passed like 'license' or 'database'
        If no kwargs is specified, it will use the default values in .config

        Parameters
        ----------
        exe : str, optional
            path to executable
        license : str, optional
            path to license file
        database : str, optional
            path to database file
        outputdirectory : str, optional
            path where to save the simulated data

        Other parameters can be used depending on the nextnano product.
        For example, 'threads' is accepted for nextnano++.
        Please, see the documentation of the command line arguments for each nextnano product
        in the website (https://www.nextnano.com/)
        """

        cmd_kwargs = dict(self.default_command_args)
        cmd_kwargs.update(kwargs)
        cmd_kwargs['inputfile'] = self.fullpath
        info = cmd_execute(**cmd_kwargs)
        self.execute_info = info
        return info

    def clear(self):
        self.raw_lines = []
        self.variables = DictList()
        self.fullpath = None

    def remove(self):
        os.remove(self.fullpath)

    def load_raw(self):
        with open(self.fullpath, 'r') as f:
            text = f.read()
        self.raw_lines = list(text_to_lines(text))
        return self.raw_lines

    def load_variables(self):
        pass

    def get_variable(self, name):
        """
        Equivalent to self.variables[name]

        Parameters
        ----------
        name : str
            key for self.variables

        Raises
        ------
        KeyError
            If name is not a key of self.variables
        """
        if name not in self.variables.keys():
            raise KeyError(f'{name} is not a valid variable.')
        return self.variables[name]

    def set_variable(self, name, value=None, comment=None):
        """
        Change the value and/or the comment of self.variable[name]

        Parameters
        ----------
        name : str
            key for self.variables
        value : not defined, optional
            Equivalent to self.variables[name].value = value (default is None)
            If it is None, it won't change it
        comment : not defined, optional
            Equivalent to self.variables[name].comment = comment (default is None)
            If it is None, it won't change it
        """

        var = self.get_variable(name)
        if value is not None:
            var.value = value
        if comment is not None:
            var.comment = comment
        return var

    def __getitem__(self, item):
        return self.variables[item]

    def __setitem__(self, item, value):
        self.variables[item] = value

    def __delitem__(self, item):
        del self.variables[item]

    def __repr__(self):
        out = []
        out.append(f'{self.__class__.__name__}')
        out.append(f'fullpath: {self.fullpath}')
        out.append(f'Input variables: {len(self.variables)} elements')
        for key, var in self.variables.items():
            out.append(f'\t{str(var)}')
        out = '\n'.join(out)
        return out

    def __iter__(self):
        self._iter_index = 0
        return self

    def __next__(self):
        try:
            result = self.variables.__getitem__(self._iter_index)
        except (IndexError, KeyError):
            raise StopIteration
        self._iter_index += 1
        return result


class InputFile(InputFileTemplate):
    # def __new__(cls, fullpath=None, configpath=None):

    def load_variables(self):
        """
        Convenient method to find the best loading method for each nextnano product.
        self.variables will be updated
        """
        _InputFile = defaults.get_InputFile(self.product)
        file = _InputFile()
        file.text = self.text
        self.variables = file.variables

class Sweep(InputFile):
    """
        This class give a user possibility to run multiple simulations (sweep) over defined variables in the input file.


        Parameters:
        -------------------
        variables_to_sweep: dict
            Dict of variables to sweep in the form of {name1:values1,name2:values2...}
            values should be an iterable object (ideally list)
        fullpath: str
            defined as for InputFile
        configpath: str
            defined as for input files


        Methods:
        --------
        save_sweep()
            creates an output folder
            creates input files for all combinations of sweep variables
        execute_sweep():
            execute created input files and saves information to output folder

    """
    def __init__(self,variables_to_sweep,fullpath=None, configpath=None):
        super().__init__(fullpath, configpath)
        if set(variables_to_sweep.keys()).issubset(self.variables.keys()):
            self.var_sweep = variables_to_sweep
        else:
            raise ValueError('Defined variables are not variables of input file')
        for value in self.var_sweep.values():
            if not isinstance(value, Iterable):
                raise TypeError('Values of variables_to_sweep should be iterable objects')
        self.sweep_output_directory = None
        self.input_files = []

    def save_sweep(self, delete_old_files = True):
        if delete_old_files == True:
            for inputfile in self.input_files:
                inputfile.remove()
        self.input_files = []
        self.create_input_files()

    def prepare_output(self, overwrite = False):
        self.sweep_output_directory = self.mk_dir(overwrite=overwrite)
        self.create_info()

    def create_input_files(self):
        iteration_combinations = list(itertools.product(*self.var_sweep.values()))
        filename_path, filename_extension = os.path.splitext(self.fullpath)
        for combination in iteration_combinations:
            filename_end = '__'
            inputfile = InputFile(fullpath = self.fullpath, configpath = self.configpath)
            for var_name, var_value in zip(self.var_sweep.keys(), combination):
                inputfile.set_variable(var_name, var_value, comment='THIS VARIABLE IS UNDER SWEEP')
                filename_end += '{}_{}_'.format(var_name, var_value)
            inputfile.save(filename_path + filename_end + filename_extension, overwrite = True)
            self.input_files.append(inputfile)


    def execute_sweep(self, delete_input_files = False, overwrite = False):
        self.prepare_output(overwrite)
        output_directory = self.sweep_output_directory
        if not self.input_files:
            warnings.warn('Nothing was executed in sweep! Input files to execute were not created.')
        for inputfile in self.input_files:
            inputfile.execute(outputdirectory = output_directory)
            if delete_input_files:
                inputfile.remove()

    def mk_dir(self,overwrite = False):
        vars = ''
        for i in self.var_sweep.keys():
            vars+=('__'+i)
        name_of_file = self.filename_only
        output_directory = self.config.get(section = self.product,option = 'outputdirectory')
        name = (name_of_file+'_sweep'+vars)
        if overwrite:
            directory = mkdir_if_not_exist(os.path.join(output_directory,name))
        else:
            directory = mkdir_even_if_exists(output_directory,name)
        return directory

    def create_info(self):
        file_location = os.path.join(self.sweep_output_directory,'sweep_info.txt')
        with open(file_location,'w') as file:
            file.write("Input file: '{}' \n".format(self.fullpath))
            file.write("Sweep variables: \n")
            for i in self.var_sweep:
                file.write("{} = {} \n".format(i,self.var_sweep[i]))