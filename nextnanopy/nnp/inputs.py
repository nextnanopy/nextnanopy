from nextnanopy.utils.mycollections import DictList
from nextnanopy.inputs import InputFileTemplate
from nextnanopy.nnp.defaults import parse_nnp_variable, is_nnp_input_text, is_nnp_variable, InputVariable_nnp


class InputFile(InputFileTemplate):
    def load_variables(self):
        variables = DictList()
        for i, line in enumerate(self.raw_lines):
            if not is_nnp_variable(line):
                continue
            name, value, comment = parse_nnp_variable(line)
            var = InputVariable_nnp(name=name, value=value, comment=comment, metadata={'line_idx': i})
            variables[var.name] = var
        self.variables = variables
        return self.variables

    def validate(self):
        if not is_nnp_input_text(self.raw_text):
            raise ValueError(f'Not valid nextnano++ input file')
