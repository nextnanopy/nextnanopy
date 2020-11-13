from nextnanopy.inputs import InputFileTemplate
from nextnanopy.msb.defaults import is_msb_input_file


class InputFile(InputFileTemplate):
    def load_variables(self):
        pass

    def validate(self):
        if not is_msb_input_file(self.fullpath):
            raise ValueError(f'Not valid nextnano.MSB input file')
