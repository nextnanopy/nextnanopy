import unittest
from nextnanopy.utils.formatting import best_str_to_name_unit, str_to_name_unit, str_to_name_unit_with_rest


class TestNameUnit(unittest.TestCase):
    def test_str_to_name_unit(self):
        self.assertEqual(str_to_name_unit('test', init='[', end=']'), ('test', None))
        self.assertEqual(str_to_name_unit('test[', init='[', end=']'), ('test[', None))
        self.assertEqual(str_to_name_unit('test[eV', init='[', end=']'), ('test[eV', None))
        self.assertEqual(str_to_name_unit('test [eV', init='[', end=']'), ('test [eV', None))
        self.assertEqual(str_to_name_unit('test [eV]', init='[', end=']'), ('test', 'eV'))
        self.assertEqual(str_to_name_unit('test [eV] another[eV]', init='[', end=']'), ('test', 'eV'))
        self.assertEqual(str_to_name_unit('test eV] ', init='[', end=']'), ('test eV]', None))
        self.assertEqual(str_to_name_unit('test[eV]_weird', init='[', end=']', add_rest_to_name=False), ('test', 'eV'))
        self.assertEqual(str_to_name_unit('test[eV]_weird', init='[', end=']', add_rest_to_name=True),
                         ('test_weird', 'eV'))
        self.assertEqual(str_to_name_unit('test [eV] _weird', init='[', end=']', add_rest_to_name=False),
                         ('test', 'eV'))
        self.assertEqual(str_to_name_unit('test [eV] _weird', init='[', end=']', add_rest_to_name=True),
                         ('test _weird', 'eV'))

        self.assertEqual(str_to_name_unit('test (eV]', init='[', end=']'), ('test (eV]', None))
        self.assertEqual(str_to_name_unit('test (eV)', init='[', end=']'), ('test (eV)', None))
        self.assertEqual(str_to_name_unit('test (eV)', init='(', end=')'), ('test', 'eV'))

    def test_str_to_name_unit_with_rest(self):
        self.assertEqual(str_to_name_unit_with_rest('test', init='[', end=']'), ('test', None))
        self.assertEqual(str_to_name_unit_with_rest('test[', init='[', end=']'), ('test[', None))
        self.assertEqual(str_to_name_unit_with_rest('test[eV', init='[', end=']'), ('test[eV', None))
        self.assertEqual(str_to_name_unit_with_rest('test [eV', init='[', end=']'), ('test [eV', None))
        self.assertEqual(str_to_name_unit_with_rest('test [eV]', init='[', end=']'), ('test', 'eV'))
        self.assertEqual(str_to_name_unit_with_rest('test [eV] another[eV]', init='[', end=']'), ('test another', 'eV'))
        self.assertEqual(str_to_name_unit_with_rest('test eV] ', init='[', end=']'), ('test eV]', None))
        self.assertEqual(str_to_name_unit_with_rest('test[eV]_weird', init='[', end=']'), ('test_weird', 'eV'))
        self.assertEqual(str_to_name_unit_with_rest('test [eV] _weird', init='[', end=']'), ('test _weird', 'eV'))

        self.assertEqual(str_to_name_unit_with_rest('test (eV]', init='[', end=']'), ('test (eV]', None))
        self.assertEqual(str_to_name_unit_with_rest('test (eV)', init='[', end=']'), ('test (eV)', None))
        self.assertEqual(str_to_name_unit_with_rest('test (eV)', init='(', end=')'), ('test', 'eV'))

    def test_best_str_to_name_unit(self):
        self.assertEqual(best_str_to_name_unit('test'), ('test', None))
        self.assertEqual(best_str_to_name_unit('test['), ('test[', None))
        self.assertEqual(best_str_to_name_unit('test[eV'), ('test[eV', None))
        self.assertEqual(best_str_to_name_unit('test [eV'), ('test [eV', None))
        self.assertEqual(best_str_to_name_unit('test [eV]'), ('test', 'eV'))
        self.assertEqual(best_str_to_name_unit('test [eV] another[eV]'), ('test another', 'eV'))
        self.assertEqual(best_str_to_name_unit('test eV] '), ('test eV]', None))
        self.assertEqual(best_str_to_name_unit('test[eV]_weird'), ('test_weird', 'eV'))
        self.assertEqual(best_str_to_name_unit('test [eV] _weird'), ('test _weird', 'eV'))

        self.assertEqual(best_str_to_name_unit('test (eV]'), ('test (eV]', None))
        self.assertEqual(best_str_to_name_unit('test (eV)'), ('test', 'eV'))
        self.assertEqual(best_str_to_name_unit('test (eV)'), ('test', 'eV'))


if __name__ == '__main__':
    unittest.main()
