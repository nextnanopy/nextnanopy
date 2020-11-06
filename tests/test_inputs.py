import unittest
import os
from nextnanopy.inputs import *
from nextnanopy.utils.formatting import is_nn3_input_file, is_nnp_input_file

folder_nnp = os.path.join('tests', 'datafiles', 'nextnano++')
folder_nn3 = os.path.join('tests', 'datafiles', 'nextnano3')

class Test_nnp(unittest.TestCase):
    def test_load(self):
        fullpath = os.path.join(folder_nnp, 'only_variables.in')

        file = InputFile(fullpath)
        self.assertEqual(file.type, 'nextnano++')

        self.assertEqual(len(file.variables.keys()), 7)
        self.assertEqual(file.variables['float'].name, 'float')
        self.assertEqual(file.variables['float'].value, float(0.0))
        self.assertEqual(file.variables['float'].comment, 'float number (a.u)')

        self.assertEqual(file.variables['int'].name, 'int')
        self.assertEqual(file.variables['int'].value, int(0))
        self.assertEqual(file.variables['int'].comment, 'int number (random = 3)')

        self.assertEqual(file.variables['str'].name, 'str')
        self.assertEqual(file.variables['str'].value, '"test"')
        self.assertEqual(file.variables['str'].comment, 'first comments # second comment')

        self.assertEqual(file.variables['reference'].name, 'reference')
        self.assertEqual(file.variables['reference'].value, '$int - 1')

        self.assertEqual(file.variables['NoSpacing'].name, 'NoSpacing')
        self.assertEqual(file.variables['NoSpacing'].value, int('7'))
        self.assertEqual(file.variables['NoSpacing'].comment, 'this is a comment')

        self.assertEqual(file.variables['MAYUS'].name, 'MAYUS')
        self.assertEqual(file.variables['MAYUS'].value, 'TEXT')
        self.assertEqual(file.variables['MAYUS'].comment, '')

        fullpath = os.path.join(folder_nnp, 'virtual_file.in')
        self.assertRaises(FileNotFoundError, InputFile, fullpath)

    def test_set_variables(self):
        fullpath = os.path.join(folder_nnp, 'only_variables.in')
        file = InputFile(fullpath)
        file.set_variable('float', 1e-5, 'some comment')

        self.assertEqual(file.variables['float'].name, 'float')
        self.assertEqual(file.variables['float'].value, 1e-5)
        self.assertEqual(file.variables['float'].comment, 'some comment')
        self.assertEqual(file.variables['float'].text, f'$float = {str(1e-5)} # some comment')
        self.assertEqual(file.lines[3], f'$float = {str(1e-5)} # some comment')

        file.set_variable('float', value=1e-7)
        self.assertEqual(file.variables['float'].name, 'float')
        self.assertEqual(file.variables['float'].value, 1e-7)
        self.assertEqual(file.variables['float'].comment, 'some comment')
        self.assertEqual(file.variables['float'].text, f'$float = {str(1e-7)} # some comment')
        self.assertEqual(file.lines[3], f'$float = {str(1e-7)} # some comment')

        file.set_variable('float', comment='new comment')
        self.assertEqual(file.variables['float'].name, 'float')
        self.assertEqual(file.variables['float'].value, 1e-7)
        self.assertEqual(file.variables['float'].comment, 'new comment')
        self.assertEqual(file.variables['float'].text, f'$float = {str(1e-7)} # new comment')
        self.assertEqual(file.lines[3], f'$float = {str(1e-7)} # new comment')

        self.assertRaises(KeyError, file.set_variable, name='new_variable')

    def test_fullpath(self):
        fullpath = os.path.join(folder_nnp, 'only_variables.in')
        file = InputFile(fullpath)

        self.assertEqual(file.fullpath, fullpath)
        self.assertEqual(file.save(file.fullpath, overwrite=False),
                         os.path.join(folder_nnp, 'only_variables_0.in'))
        os.remove(file.fullpath)


class Test_nn3(unittest.TestCase):
    def test_load(self):
        fullpath = os.path.join(folder_nn3, 'only_variables.in')
        self.assertTrue(is_nn3_input_file(fullpath))

        file = InputFile(fullpath)
        self.assertEqual(file.type, 'nextnano3')

        self.assertEqual(len(file.variables.keys()), 7)
        self.assertEqual(file.variables['float'].name, 'float')
        self.assertEqual(file.variables['float'].value, float(0.0))
        self.assertEqual(file.variables['float'].comment, 'float number (a.u)')

        self.assertEqual(file.variables['int'].name, 'int')
        self.assertEqual(file.variables['int'].value, int(0))
        self.assertEqual(file.variables['int'].comment, 'int number (random = 3)')

        self.assertEqual(file.variables['str'].name, 'str')
        self.assertEqual(file.variables['str'].value, '"test"')
        self.assertEqual(file.variables['str'].comment, 'first comments # second comment')

        self.assertEqual(file.variables['reference'].name, 'reference')
        self.assertEqual(file.variables['reference'].value, '$int - 1')

        self.assertEqual(file.variables['NoSpacing'].name, 'NoSpacing')
        self.assertEqual(file.variables['NoSpacing'].value, int('7'))
        self.assertEqual(file.variables['NoSpacing'].comment, 'this is a comment')

        self.assertEqual(file.variables['MAYUS'].name, 'MAYUS')
        self.assertEqual(file.variables['MAYUS'].value, 'TEXT')
        self.assertEqual(file.variables['MAYUS'].comment, '')

        fullpath = os.path.join(folder_nn3, 'virtual_file.in')
        self.assertRaises(FileNotFoundError, InputFile, fullpath)

    def test_set_variables(self):
        fullpath = os.path.join(folder_nn3,  'only_variables.in')
        file = InputFile(fullpath)
        file.set_variable('float', 1e-5, 'some comment')

        self.assertEqual(file.variables['float'].name, 'float')
        self.assertEqual(file.variables['float'].value, 1e-5)
        self.assertEqual(file.variables['float'].comment, 'some comment')
        self.assertEqual(file.variables['float'].text, f'%float = {str(1e-5)} ! some comment')
        self.assertEqual(file.lines[3], f'%float = {str(1e-5)} ! some comment')

        file.set_variable('float', value=1e-7)
        self.assertEqual(file.variables['float'].name, 'float')
        self.assertEqual(file.variables['float'].value, 1e-7)
        self.assertEqual(file.variables['float'].comment, 'some comment')
        self.assertEqual(file.variables['float'].text, f'%float = {str(1e-7)} ! some comment')
        self.assertEqual(file.lines[3], f'%float = {str(1e-7)} ! some comment')

        file.set_variable('float', comment='new comment')
        self.assertEqual(file.variables['float'].name, 'float')
        self.assertEqual(file.variables['float'].value, 1e-7)
        self.assertEqual(file.variables['float'].comment, 'new comment')
        self.assertEqual(file.variables['float'].text, f'%float = {str(1e-7)} ! new comment')
        self.assertEqual(file.lines[3], f'%float = {str(1e-7)} ! new comment')

        self.assertRaises(KeyError, file.set_variable, name='new_variable')

    def test_fullpath(self):
        fullpath = os.path.join(folder_nn3, 'only_variables.in')
        file = InputFile(fullpath)

        self.assertEqual(file.fullpath, fullpath)
        self.assertEqual(file.save(file.fullpath, overwrite=False),
                         os.path.join(folder_nn3, 'only_variables_0.in'))
        os.remove(file.fullpath)

if __name__ == '__main__':
    #
    # _folder = folder_nn3
    # fullpath = os.path.join(_folder, 'only_variables.in')
    # is_nn3_input_file(fullpath)
    # f = InputFile(fullpath)
    unittest.main()
