import unittest
import nextnanopy.commands as commands
from nextnanopy.commands import *
from nextnanopy.commands import _path, _bool

import os

folder_nnp = os.path.join('tests', 'datafiles', 'nextnano++')
folder_nn3 = os.path.join('tests', 'datafiles', 'nextnano3')
folder_negf = os.path.join('tests', 'datafiles', 'nextnano.NEGF')


class TestCommands(unittest.TestCase):

    def test_commands_nnp(self):
        self.maxDiff = None
        inputfile = os.path.join(folder_nnp, 'example.in')
        exe = os.path.join('nextnano++', 'bin 64bit', 'nextnano++_Intel_64bit.exe')
        license = os.path.join(r'nextnanopy\License', 'License_nnp.lic')
        database = os.path.join('nextnano++', 'Syntax', 'database_nnp.in')
        outputdirectory = r'tests\datafiles'
        threads = 4
        cmd = f'"{exe}" --license "{license}" --database "{database}" --threads {threads} --outputdirectory "{outputdirectory}" --noautooutdir "{inputfile}"'
        kwargs = dict(inputfile=inputfile, exe=exe, license=license, database=database, outputdirectory=outputdirectory,
                      threads=threads)
        self.assertEqual(command_nnp(**kwargs), cmd)
        self.assertEqual(command(**kwargs), cmd)

    def test_commands_nn3(self):
        self.maxDiff = None
        inputfile = os.path.join(folder_nn3, 'example.in')
        exe = os.path.join('nextnano++', 'bin 64bit', 'nextnano++_Intel_64bit.exe')
        license = os.path.join(r'nextnanopy\License', 'License_nnp.lic')
        database = os.path.join('nextnano++', 'Syntax', 'database_nnp.in')
        outputdirectory = r'tests\datafiles'
        threads = 4
        debuglevel = 0
        cancel = -1
        softkill = -1
        cmd = f'"{exe}" -license "{license}" -inputfile "{inputfile}" -database "{database}" -threads {threads} -outputdirectory "{outputdirectory}" -debuglevel {debuglevel} -cancel {cancel} -softkill {softkill}'
        kwargs = dict(inputfile=inputfile, exe=exe, license=license, database=database, outputdirectory=outputdirectory,
                      threads=threads, debuglevel=debuglevel, cancel=cancel, softkill=softkill)
        self.assertEqual(command_nn3(**kwargs), cmd)
        self.assertEqual(command(**kwargs), cmd)

    def test_commands_negf(self):
        self.maxDiff = None
        inputfile = os.path.join(folder_negf, 'example.xml')
        exe = os.path.join('nextnano.NEGF', 'nextnano.NEGF.exe')
        license = os.path.join(r'License', 'License_nnQCL.lic')
        database = os.path.join('nextnano.NEGF', 'Material_Database.xml')
        outputdirectory = r'tests\datafiles'
        threads = 4
        cmd = f'"{exe}" "{inputfile}" "{outputdirectory}" "{database}" "{license}" -threads {threads}'
        kwargs = dict(inputfile=inputfile, exe=exe, license=license, database=database, outputdirectory=outputdirectory,
                      threads=threads)
        self.assertEqual(command_negf(**kwargs), cmd)
        self.assertEqual(command(**kwargs), cmd)

    def test_path(self):
        self.assertEqual(_path('aa\nb.test'), '"aa\nb.test"')
        self.assertEqual(_path('aa\nb'), '"aa\nb"')
        self.assertEqual(_path(''), '')
        self.assertEqual(_path(2), '"2"')
        self.assertEqual(_path(None), None)

    def test_execute(self):
        self.assertRaises(ValueError, execute, inputfile='', exe='', license='', database='', outputdirectory='')
        self.assertRaises(ValueError, execute, inputfile=r'test\datafiles', exe='', license='', database='',
                          outputdirectory='')

    def test_bool(self):
        self.assertEqual(_bool(''), False)
        self.assertEqual(_bool(None), False)
        self.assertEqual(_bool('1'), True)
        self.assertEqual(_bool('0'), True)
        self.assertEqual(_bool(0), True)
        self.assertEqual(_bool(1), True)


if __name__ == '__main__':
    unittest.main()