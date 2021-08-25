import unittest
import os
from nextnanopy.inputs import InputFile, Sweep

folder_nnp = os.path.join('tests', 'datafiles', 'nextnano++')
folder_nn3 = os.path.join('tests', 'datafiles', 'nextnano3')
folder_negf = os.path.join('tests', 'datafiles', 'nextnano.NEGF')


class Test_nnp(unittest.TestCase):
    def test_load(self):
        fullpath = os.path.join(folder_nnp, 'only_variables.in')

        file = InputFile(fullpath)
        self.assertEqual(file.product, 'nextnano++')

        self.assertEqual(len(file.variables.keys()), 7)
        self.assertEqual(file.variables['float'].name, 'float')
        self.assertEqual(file.variables['float'].value, float(0.0))
        self.assertEqual(file.variables['float'].comment, 'float number (a.u.)')

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
        self.assertEqual(file.variables['NoSpacing'].text, '$NoSpacing = 7 # this is a comment')

        self.assertEqual(file.variables['MAYUS'].name, 'MAYUS')
        self.assertEqual(file.variables['MAYUS'].value, 'TEXT')
        self.assertEqual(file.variables['MAYUS'].comment, '')
        self.assertEqual(file.variables['MAYUS'].text, '$MAYUS = TEXT')

        fullpath = os.path.join(folder_nnp, 'virtual_file.in')
        self.assertRaises(FileNotFoundError, InputFile, fullpath)

    def test_get_variables(self):
        fullpath = os.path.join(folder_nn3, 'only_variables.in')
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
            self.assertEqual(file.default_command_args[key], value)

    def test_text(self):
        fullpath = os.path.join(folder_nnp, 'only_variables.in')

        file = InputFile(fullpath)
        text = file.text

        new_file = InputFile()
        self.assertEqual(new_file.product, 'not valid')
        self.assertEqual(new_file.fullpath, None)
        self.assertEqual(new_file.text, '')
        self.assertEqual(new_file.raw_lines, [])

        new_file.text = text
        self.assertEqual(new_file.product, 'nextnano++')
        self.assertEqual(new_file.fullpath, None)
        self.assertEqual(new_file.text, text)
        self.assertEqual(new_file.lines, file.lines)
        self.assertEqual(new_file.variables['MAYUS'].name, 'MAYUS')
        self.assertEqual(new_file.variables['MAYUS'].value, 'TEXT')
        self.assertEqual(new_file.variables['MAYUS'].comment, '')
        self.assertEqual(new_file.variables['MAYUS'].text, '$MAYUS = TEXT')
        self.assertRaises(ValueError, new_file.save)
        self.assertEqual(new_file.save(file.fullpath, overwrite=False),
                         os.path.join(folder_nnp, 'only_variables_0.in'))
        os.remove(new_file.fullpath)


class Test_nn3(unittest.TestCase):
    def test_load(self):
        fullpath = os.path.join(folder_nn3, 'only_variables.in')

        file = InputFile(fullpath)
        self.assertEqual(file.product, 'nextnano3')

        self.assertEqual(len(file.variables.keys()), 7)
        self.assertEqual(file.variables['float'].name, 'float')
        self.assertEqual(file.variables['float'].value, float(0.0))
        self.assertEqual(file.variables['float'].comment, 'float number (a.u.)')

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
        fullpath = os.path.join(folder_nn3, 'only_variables.in')
        file = InputFile(fullpath)

        self.assertEqual(file.variables['float'], file.get_variable('float'))
        self.assertRaises(KeyError, file.get_variable, name='new_variable')

    def test_set_variables(self):
        fullpath = os.path.join(folder_nn3, 'only_variables.in')
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
            self.assertEqual(file.default_command_args[key], value)

    def test_save(self):
        fullpath = os.path.join(folder_nn3, 'only_variables.in')
        file = InputFile(fullpath)
        new_folder = os.path.join(folder_nn3, 'temp')
        new_file = os.path.join(new_folder, 'example_copy.in')
        self.assertRaises(FileNotFoundError, file.save, new_file, overwrite=True, automkdir=False)
        self.assertEqual(file.save(new_file, overwrite=True, automkdir=True), new_file)
        os.remove(file.fullpath)
        os.rmdir(new_folder)

    def test_text(self):
        fullpath = os.path.join(folder_nn3, 'only_variables.in')

        file = InputFile(fullpath)
        text = file.text

        new_file = InputFile()
        self.assertEqual(new_file.product, 'not valid')
        self.assertEqual(new_file.fullpath, None)
        self.assertEqual(new_file.text, '')
        self.assertEqual(new_file.raw_lines, [])

        new_file.text = text
        self.assertEqual(new_file.product, 'nextnano3')
        self.assertEqual(new_file.fullpath, None)
        self.assertEqual(new_file.text, text)
        self.assertEqual(new_file.lines, file.lines)
        self.assertEqual(new_file.variables['MAYUS'].name, 'MAYUS')
        self.assertEqual(new_file.variables['MAYUS'].value, 'TEXT')
        self.assertEqual(new_file.variables['MAYUS'].comment, '')
        self.assertEqual(new_file.variables['MAYUS'].text, '%MAYUS = TEXT')
        self.assertRaises(ValueError, new_file.save)
        self.assertEqual(new_file.save(file.fullpath, overwrite=False),
                         os.path.join(folder_nn3, 'only_variables_0.in'))
        os.remove(new_file.fullpath)


class Test_negf(unittest.TestCase):
    def test_load(self):
        fullpath = os.path.join(folder_negf, 'example.xml')

        file = InputFile(fullpath)
        self.assertEqual(file.product, 'nextnano.NEGF')

        self.assertEqual(len(file.variables.keys()), 0)

        fullpath = os.path.join(folder_negf, 'virtual_file.xml')
        self.assertRaises(FileNotFoundError, InputFile, fullpath)

    def test_set_variables(self):
        fullpath = os.path.join(folder_negf, 'example.xml')
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
            self.assertEqual(file.default_command_args[key], value)


class TestInputFile(unittest.TestCase):

    def test_access_by_index(self):
        fullpath = os.path.join(folder_nnp, 'only_variables.in')
        file = InputFile(fullpath)
        for key, value in file.variables.items():
            self.assertEqual(file[key], value)

    def test_for_loop(self):
        fullpath = os.path.join(folder_nnp, 'only_variables.in')
        file = InputFile(fullpath)
        for i, fi in enumerate(file):
            self.assertEqual(file.variables[i], fi)

    def test_fullpath(self):
        fullpath = os.path.join(folder_nnp, 'only_variables.in')
        file = InputFile(fullpath)
        self.assertEqual(file.fullpath, fullpath)
        self.assertEqual(file.filename, 'only_variables.in')
        self.assertEqual(file.filename_only, 'only_variables')
        self.assertEqual(file.folder_input, folder_nnp)
        self.assertEqual(file.execute_info, {})

        file.filename = 'new_name.in'
        self.assertEqual(file.filename, 'new_name.in')
        self.assertEqual(file.filename_only, 'new_name')
        self.assertEqual(file.fullpath, os.path.join(folder_nnp, 'new_name.in'))
        self.assertEqual(file.folder_input, folder_nnp)

        file.filename_only = 'another_filename'
        self.assertEqual(file.filename, 'another_filename.in')
        self.assertEqual(file.filename_only, 'another_filename')
        self.assertEqual(file.fullpath, os.path.join(folder_nnp, 'another_filename.in'))
        self.assertEqual(file.folder_input, folder_nnp)

        npath = os.path.join('new','folder')
        file.folder_input = npath
        self.assertEqual(file.filename, 'another_filename.in')
        self.assertEqual(file.filename_only, 'another_filename')
        self.assertEqual(file.fullpath, os.path.join(npath, 'another_filename.in'))
        self.assertEqual(file.folder_input, npath)

        npath = os.path.join('random', 'path')
        file.execute_info['outputdirectory'] = npath
        self.assertEqual(file.folder_output, npath)

class TestSweep(unittest.TestCase):

    def test_init(self):
        self.assertRaises(TypeError, Sweep)
        sweep = Sweep({})
        self.assertEqual(sweep.fullpath, None)
        self.assertEqual(sweep.var_sweep, {})
        self.assertRaises(ValueError, Sweep, {'Name': 'some_name'})



    def test_nnp_init(self):
        fullpath = os.path.join(folder_nnp, 'only_variables.in')
        self.assertRaises(ValueError, Sweep, {'Name': 'some_name'}, fullpath)

        sweep = Sweep({},fullpath)
        self.assertEqual(sweep.fullpath, fullpath)
        self.assertEqual(sweep.var_sweep, {})
        self.assertFalse(sweep.input_files)
        self.assertFalse(sweep.sweep_output_directory)


        self.assertRaises(ValueError, Sweep, {'float':1})
        self.assertRaises(TypeError, Sweep, {'float': 1}, fullpath)

        sweep = Sweep({'float': [1,2,5]}, fullpath)
        self.assertEqual(sweep.fullpath, fullpath)
        self.assertEqual(sweep.var_sweep['float'],[1,2,5])

    def test_nnp_mkdir(self):
        fullpath = os.path.join(folder_nnp, 'only_variables.in')
        sweep = Sweep({},fullpath = fullpath)
        sweep.config.set('nextnano++','outputdirectory',r'tests//outputs')
        self.assertEqual(os.path.join(sweep.mk_dir(overwrite=True)), r'tests//outputs\only_variables_sweep')
        self.addCleanup(os.rmdir,r'tests//outputs\only_variables_sweep')




if __name__ == '__main__':
    unittest.main()

    file = os.path.join(folder_nnp, 'only_variables.in')
    fi = InputFile(file)
    text = fi.text
