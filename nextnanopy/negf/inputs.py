from nextnanopy.inputs import InputFileTemplate
from nextnanopy.negf.defaults import is_negf_input_text
from nextnanopy.nnp.defaults import (
    InputVariable_nnp,
    is_nnp_variable,
    parse_nnp_variable,
)
from nextnanopy.utils.mycollections import DictList


class InputFile(InputFileTemplate):
    def load_variables(self):
        variables = DictList()
        for i, line in enumerate(self.raw_lines):
            if not is_nnp_variable(line):
                continue
            name, value, comment = parse_nnp_variable(line)
            var = InputVariable_nnp(
                name=name, value=value, comment=comment, metadata={"line_idx": i}
            )
            variables[var.name] = var
        self.variables = variables
        return self.variables

    def validate(self):
        if not is_negf_input_text(self.raw_text):
            raise ValueError("Not a valid nextnano.NEGF++ input file")
