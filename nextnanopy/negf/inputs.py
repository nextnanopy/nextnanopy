from nextnanopy.inputs import InputFileTemplate
from nextnanopy.negf.defaults import is_negf_input_file


class InputFile(InputFileTemplate):
    def load_variables(self):
        pass

    def validate(self):
        if not is_negf_input_file(self.fullpath):
            raise ValueError(f'Not valid nextnano.NEGF input file')
