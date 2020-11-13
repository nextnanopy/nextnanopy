import unittest
import os
from nextnanopy.inputs import InputFile

folder_nnp = os.path.join('tests', 'datafiles', 'nextnano++')
folder_nn3 = os.path.join('tests', 'datafiles', 'nextnano3')
folder_negf = os.path.join('tests', 'datafiles', 'nextnano.NEGF')

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

    def test_get_variables(self):
        fullpath = os.path.join(folder_nn3,  'only_variables.in')
        file = InputFile(fullpath)

        self.assertEqual(file.variables['float'], file.get_variable('float'))
        self.assertRaises(KeyError, file.get_variable, name='new_variable')

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

        file.set_variable('float', value=0)
        self.assertEqual(file.variables['float'].value, 0)
        file.set_variable('float', value='0')
        self.assertEqual(file.variables['float'].value, '0')
        self.assertRaises(KeyError, file.set_variable, name='new_variable')
        self.assertRaises(KeyError, file.set_variable, name='new_variable')

    def test_fullpath(self):
        fullpath = os.path.join(folder_nnp, 'only_variables.in')
        file = InputFile(fullpath)

        self.assertEqual(file.fullpath, fullpath)
        self.assertEqual(file.save(file.fullpath, overwrite=False),
                         os.path.join(folder_nnp, 'only_variables_0.in'))
        os.remove(file.fullpath)

    def test_config(self):
        fullpath = os.path.join(folder_nnp, 'only_variables.in')
        file = InputFile(fullpath)
        from nextnanopy import config
        for key, value in config.config['nextnano++'].items():
            self.assertEqual(file.default_command_args[key],value)

class Test_nn3(unittest.TestCase):
    def test_load(self):
        fullpath = os.path.join(folder_nn3, 'only_variables.in')

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

    def test_get_variables(self):
        fullpath = os.path.join(folder_nn3,  'only_variables.in')
        file = InputFile(fullpath)

        self.assertEqual(file.variables['float'], file.get_variable('float'))
        self.assertRaises(KeyError, file.get_variable, name='new_variable')

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

        file.set_variable('float', value=0)
        self.assertEqual(file.variables['float'].value, 0)
        file.set_variable('float', value='0')
        self.assertEqual(file.variables['float'].value, '0')
        self.assertRaises(KeyError, file.set_variable, name='new_variable')

    def test_fullpath(self):
        fullpath = os.path.join(folder_nn3, 'only_variables.in')
        file = InputFile(fullpath)

        self.assertEqual(file.fullpath, fullpath)
        self.assertEqual(file.save(file.fullpath, overwrite=False),
                         os.path.join(folder_nn3, 'only_variables_0.in'))
        os.remove(file.fullpath)

    def test_config(self):
        fullpath = os.path.join(folder_nn3, 'only_variables.in')
        file = InputFile(fullpath)
        from nextnanopy import config
        for key, value in config.config['nextnano3'].items():
            self.assertEqual(file.default_command_args[key],value)

    def test_save(self):
        fullpath = os.path.join(folder_nn3, 'only_variables.in')
        file = InputFile(fullpath)
        new_folder = os.path.join(folder_nn3,'temp')
        new_file = os.path.join(new_folder, 'example_copy.in')
        self.assertRaises(FileNotFoundError, file.save, new_file, overwrite=True, automkdir=False)
        self.assertEqual(file.save(new_file, overwrite=True, automkdir=True),new_file)
        os.remove(file.fullpath)
        os.rmdir(new_folder)

class Test_negf(unittest.TestCase):
    def test_load(self):
        fullpath = os.path.join(folder_negf, 'example.xml')

        file = InputFile(fullpath)
        self.assertEqual(file.type, 'nextnano.NEGF')

        self.assertEqual(len(file.variables.keys()), 0)

        fullpath = os.path.join(folder_negf, 'virtual_file.xml')
        self.assertRaises(FileNotFoundError, InputFile, fullpath)

    def test_set_variables(self):
        fullpath = os.path.join(folder_negf,  'example.xml')
        file = InputFile(fullpath)
        self.assertRaises(KeyError, file.set_variable, name='new_variable')

    def test_fullpath(self):
        fullpath = os.path.join(folder_negf, 'example.xml')
        file = InputFile(fullpath)

        self.assertEqual(file.fullpath, fullpath)
        self.assertEqual(file.save(file.fullpath, overwrite=False),
                         os.path.join(folder_negf, 'example_0.xml'))
        os.remove(file.fullpath)

    def test_config(self):
        fullpath = os.path.join(folder_negf, 'example.xml')
        file = InputFile(fullpath)
        from nextnanopy import config
        for key, value in config.config['nextnano.NEGF'].items():
            self.assertEqual(file.default_command_args[key],value)


if __name__ == '__main__':
    unittest.main()
