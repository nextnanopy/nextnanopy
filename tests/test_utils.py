import unittest
from nextnanopy.utils import mycollections
import os
from nextnanopy.utils.formatting import (fmts, is_nn3_input_file, is_nnp_input_file,
                                         is_negf_input_file, input_file_type)

folder_nnp = os.path.join('tests', 'datafiles', 'nextnano++')
folder_nn3 = os.path.join('tests', 'datafiles', 'nextnano3')
folder_negf = os.path.join('tests', 'datafiles', 'nextnano.NEGF')


class TestDictlist(unittest.TestCase):
    def test_dictlist(self):
        a = mycollections.DictList(a=2, b=3, c=4)
        self.assertEqual(a[0], 2)
        self.assertEqual(a['a'], 2)
        self.assertEqual(a[1], 3)
        self.assertEqual(a['b'], 3)
        self.assertEqual(list(a.keys()), ['a', 'b', 'c'])
        self.assertEqual(list(a.values()), [2, 3, 4])


class TestFormatting(unittest.TestCase):
    def test_nn3(self):
        fullpath = os.path.join(folder_nn3, 'example.in')
        self.assertTrue(is_nn3_input_file(fullpath))
        self.assertFalse(is_nnp_input_file(fullpath))
        self.assertFalse(is_negf_input_file(fullpath))
        self.assertEqual(input_file_type(fullpath), 'nextnano3')
        self.assertEqual(fmts['nextnano3']['var_char'], '%')
        self.assertEqual(fmts['nextnano3']['com_char'], '!')
        self.assertEqual(fmts['nextnano3']['input_pattern'], '$end_simulation-dimension')

    def test_nnp(self):
        fullpath = os.path.join(folder_nnp, 'example.in')
        self.assertTrue(is_nnp_input_file(fullpath))
        self.assertFalse(is_nn3_input_file(fullpath))
        self.assertFalse(is_negf_input_file(fullpath))
        self.assertEqual(input_file_type(fullpath), 'nextnano++')
        self.assertEqual(fmts['nextnano++']['var_char'], '$')
        self.assertEqual(fmts['nextnano++']['com_char'], '#')
        self.assertEqual(fmts['nextnano++']['input_pattern'], 'global{')

    def test_negf(self):
        fullpath = os.path.join(folder_negf, 'example.xml')
        self.assertFalse(is_nnp_input_file(fullpath))
        self.assertFalse(is_nn3_input_file(fullpath))
        self.assertTrue(is_negf_input_file(fullpath))
        self.assertEqual(input_file_type(fullpath), 'nextnano.NEGF')
        self.assertEqual(fmts['nextnano.NEGF']['var_char'], 'NOT DEFINED')
        self.assertEqual(fmts['nextnano.NEGF']['com_char'], '<!--')
        self.assertEqual(fmts['nextnano.NEGF']['input_pattern'], '<Simulation')


if __name__ == '__main__':
    unittest.main()
