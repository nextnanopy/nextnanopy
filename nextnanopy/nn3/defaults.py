from nextnanopy.utils.datasets import InputVariable
from nextnanopy.utils.formatting import str_to_path, _path, pattern_in_file, is_variable, parse_variable, \
    generate_command, pattern_in_text
from collections import OrderedDict

fmt = {
    'var_char': '%',
    'com_char': '!',
    'input_pattern': '$end_simulation-dimension',
}

config_validator = {
    'exe': str_to_path,
    'license': str_to_path,
    'database': str_to_path,
    'threads': int,
    'outputdirectory': str_to_path,
    'debuglevel': int,
    'cancel': int,
    'softkill': int,
}

config_default = {
    'exe': '',
    'license': '',
    'database': '',
    'threads': 0,
    'outputdirectory': '',
    'debuglevel': 0,
    'cancel': -1,
    'softkill': -1,
}


"""
The option 'system' should be implemented once we convince that everyone uses the later version of nn3 than 2021_12_24.
Also the default value of debuglevel should be a negative integer. (i.e. ignore the flag)
We only need to comment out the 3 corresponding lines.

About the difference of '-...' and '--...', '--license' will also work and should be the new default.
For backwards compatibility, we keep '-license' for the moment.
"""
def command_nn3(
        inputfile,
        exe,
        license,
        database,
        outputdirectory,
        threads=0,
        debuglevel=0,
        #dubuglevel=-1,             # pending change
        cancel=-1,
        softkill=-1,
        #system='default',          # pending change
        **kwargs,
):
    kwargs = OrderedDict(
        exe=[_path(exe), ''],
        license=['-license', _path(license)],
        inputfile=['-inputfile', _path(inputfile)],
        database=['-database', _path(database)],
        threads=['-threads', threads],
        outputdirectory=['-outputdirectory', _path(outputdirectory)],
        debuglevel=['-debuglevel', debuglevel],
        cancel=['-cancel', cancel],
        softkill=['-softkill', softkill],
        #system=['-system', system],        # pending change
        no_file_options=[kwargs['no_file_options'], ''] if 'no_file_options' in kwargs else ['', ''],
    )
    return generate_command(kwargs.values())


def is_nn3_variable(text):
    return is_variable(text, var_char=fmt['var_char'])


def parse_nn3_variable(text):
    return parse_variable(text, var_char=fmt['var_char'], com_char=fmt['com_char'])


def is_nn3_input_file(fullpath):
    return pattern_in_file(fullpath, fmt['input_pattern'])


def is_nn3_input_text(text):
    return pattern_in_text(text, fmt['input_pattern'])


class InputVariable_nn3(InputVariable):
    var_char = fmt['var_char']
    com_char = fmt['com_char']
