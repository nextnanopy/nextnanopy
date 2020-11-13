from nextnanopy.utils.datasets import InputVariable
from nextnanopy.utils.formatting import str_to_path, _path, pattern_in_file, is_variable, parse_variable, \
    generate_command
from collections import OrderedDict

fmt = {
    'var_char': '$',
    'com_char': '#',
    'input_pattern': 'global{',
}

config_validator = {
    'exe': str_to_path,
    'license': str_to_path,
    'database': str_to_path,
    'outputdirectory': str_to_path,
    'threads': int,
}

config_default = {
    'exe': '',
    'license': '',
    'database': '',
    'outputdirectory': '',
    'threads': 0,
}


def command_nnp(
        inputfile,
        exe,
        license,
        database,
        outputdirectory,
        threads=0,
        **kwargs,
):
    kwargs = OrderedDict(
        exe=[_path(exe), ''],
        license=['--license', _path(license)],
        database=['--database', _path(database)],
        threads=['--threads', threads],
        outputdirectory=['--outputdirectory', _path(outputdirectory)],
        noautooutdir=['--noautooutdir', ''],
        inputfile=[_path(inputfile), ''],
    )
    return generate_command(kwargs.values())


def is_nnp_variable(text):
    return is_variable(text, var_char=fmt['var_char'])


def parse_nnp_variable(text):
    return parse_variable(text, var_char=fmt['var_char'], com_char=fmt['com_char'])


def is_nnp_input_file(fullpath):
    return pattern_in_file(fullpath, fmt['input_pattern'])


class InputVariable_nnp(InputVariable):
    var_char = fmt['var_char']
    com_char = fmt['com_char']
