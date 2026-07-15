from collections import OrderedDict

from nextnanopy.utils.formatting import (
    _path,
    generate_command,
    is_variable,
    parse_variable,
    pattern_in_text,
)

fmt = {
    "var_char": "$",
    "com_char": "#",
    "input_pattern": "nextnano.MSB{",
}

# Only options whose raw config string needs converting to another type get a
# validator. Path options (exe/license/database/outputdirectory) are kept verbatim:
# no useful validation exists at config-load time (see decisions_later.md), and their
# absence here means validate_config() passes them through untouched.
config_validator = {
    "debug": int,
}

config_default = {
    "exe": "",
    "license": "",
    "database": "",
    "outputdirectory": "",
    "debug": 0,
}


def command_msb(
    inputfile,
    exe,
    license,
    database,
    outputdirectory,
    threads=0,
    **kwargs,
):
    kwargs = OrderedDict(
        exe=[_path(exe), ""],
        runmode=[kwargs["runmode"], ""] if "runmode" in kwargs else ["", ""],
        license=["--license", _path(license)],
        database=["--database", _path(database)],
        threads=["--threads", threads],
        outputdirectory=["--outputdirectory", _path(outputdirectory)],
        noautooutdir=["--noautooutdir", ""],
        no_file_options=[kwargs["no_file_options"], ""]
        if "no_file_options" in kwargs
        else ["", ""],
        inputfile=[_path(inputfile), ""],
    )
    return generate_command(kwargs.values())


def is_msb_variable(text):
    return is_variable(text, var_char=fmt["var_char"])


def parse_msb_variable(text):
    return parse_variable(text, var_char=fmt["var_char"], com_char=fmt["com_char"])


def is_msb_input_text(text):
    return pattern_in_text(text, fmt["input_pattern"])
