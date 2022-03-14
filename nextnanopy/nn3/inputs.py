from nextnanopy.utils.mycollections import DictList
from nextnanopy.inputs import InputFileTemplate
from nextnanopy.nn3.defaults import parse_nn3_variable, is_nn3_input_text, is_nn3_variable, InputVariable_nn3


class InputFile(InputFileTemplate):
    def load_variables(self):
        variables = DictList()
        for i, line in enumerate(self.raw_lines):
            if not is_nn3_variable(line):
                continue
            name, value, comment = parse_nn3_variable(line)
            var = InputVariable_nn3(name=name, value=value, comment=comment, metadata={'line_idx': i})
            variables[var.name] = var
        self.variables = variables
        return self.variables

    def validate(self):
        if not is_nn3_input_text(self.raw_text):
            raise ValueError(f'Not valid nextnano3 input file')
