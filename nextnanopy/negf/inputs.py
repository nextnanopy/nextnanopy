from nextnanopy.utils.mycollections import DictList
from nextnanopy.inputs import InputFileTemplate
from nextnanopy.negf.defaults import is_negf_input_text, InputVariable_NEGF, parse_negf_variable_name

import xml.etree.ElementTree as ET

class InputFile(InputFileTemplate):
    def load_variables(self):
        root = ET.fromstring(self.text)
        varsection = root.find('Variables')
        variables = DictList()
        if not varsection:
            self.variables = variables
            return self.variables
        vars = varsection.findall('Constant')


        for var in vars:
            name_element = var.find('Name')
            name = parse_negf_variable_name(name_element.text)
            comment = name_element.get('Comment')

            value_element = var.find('Value')
            value = float(value_element.text)
            unit = value_element.get('Unit')
            var = InputVariable_NEGF(name=name, value=value, unit = unit,  comment=comment)
            variables[name] = var
        self.variables = variables
        return self.variables





    def validate(self):
        if not is_negf_input_text(self.raw_text):
            raise ValueError(f'Not valid nextnano.NEGF input file')
