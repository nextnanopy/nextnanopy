from collections import OrderedDict

from nextnanopy.utils.datasets import InputVariable
from nextnanopy.utils.formatting import (
    _path,
    generate_command,
    is_variable,
    pattern_in_text,
)

fmt_classic = {
    "var_char": "$",
    "com_char": "<!--",
    "input_pattern": "<Simulation",
}

fmt = {
    "var_char": "$",
    "com_char": "#",
    "input_pattern": "nextnano.NEGF{",
}

# Only options whose raw config string needs converting to another type get a
# validator. Path options (exe/license/database/outputdirectory) are kept verbatim:
# no useful validation exists at config-load time (see decisions_later.md), and their
# absence here means validate_config() passes them through untouched.
config_validator = {
    "threads": int,
}

config_default = {
    "exe": "",
    "license": "",
    "database": "",
    "outputdirectory": "",
    "threads": 0,
}


def command_negf_classic(
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
        inputfile=[_path(inputfile), ""],
        outputdirectory=[_path(outputdirectory), ""],
        database=[_path(database), ""],
        license=[_path(license), ""],
        threads=["-threads", threads],
    )
    return generate_command(kwargs.values())


def command_negf(
    inputfile,
    exe,
    license,
    database,
    outputdirectory,
    threads=0,
    debug_output_specifications=None,
    **kwargs,
):
    kwargs = OrderedDict(
        exe=[_path(exe), ""],
        inputfile=["--input-file", _path(inputfile)],
        outputdirectory=["--outputdirectory", _path(outputdirectory)],
        database=["--database", _path(database)],
        license=["--license", _path(license)],
        threads=["--threads", threads],
    )
    if debug_output_specifications is not None:
        kwargs["debug"] = ["--debug", debug_output_specifications]
        kwargs.move_to_end("debug")
    return generate_command(kwargs.values())


def is_negf_variable(text):
    return is_variable(text, var_char=fmt_classic["var_char"])


# def parse_negf_variable(text):
#    return parse_variable(text, var_char=fmt['var_char'], com_char=fmt['com_char'])


def parse_negf_variable_name(text):
    if text.startswith(fmt_classic["var_char"]):
        return text[1:]
    else:
        raise ValueError(f"variable name in NEGF should start with {fmt_classic['var_char']}")


def is_negf_classic_input_text(text):
    return pattern_in_text(text, fmt_classic["input_pattern"])


def is_negf_input_text(text):
    return pattern_in_text(text, fmt["input_pattern"])


class InputVariable_NEGF(InputVariable):
    var_char = fmt_classic["var_char"]

    @property
    def text(self):
        t = f"{self.var_char}{self.name} = {self.value} {self.unit}"
        if self.comment:
            t = f"{t} Comment: {self.comment}"
        return t
