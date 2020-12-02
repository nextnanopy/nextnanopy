import unittest
from nextnanopy.utils.datasets import Data, Variable, Coord
from nextnanopy.utils.datasets import default_unit
import numpy as np


class TestDatasets(unittest.TestCase):
    def test_Data(self):
        ds = Data(name='test', value=2)
        self.assertEqual(ds.name, 'test')
        self.assertEqual(ds.value, np.array(2))
        self.assertEqual(ds.unit, default_unit)
        self.assertEqual(ds.metadata, {})

    def test_Variable(self):
        ds = Variable(name='test', value=2)
        self.assertEqual(ds.name, 'test')
        self.assertEqual(ds.value, np.array(2))
        self.assertEqual(ds.unit, default_unit)
        self.assertEqual(ds.metadata, {})

    def test_Coord(self):
        ds = Coord(name='test', value=2, dim=3, offset=10)
        self.assertEqual(ds.name, 'test')
        self.assertEqual(ds.value, np.array(2))
        self.assertEqual(ds.unit, default_unit)
        self.assertEqual(ds.metadata, {})
        self.assertEqual(ds.dim, 3)
        self.assertEqual(ds.offset, np.array(10))
        self.assertEqual(ds.get_value(use_offset=True), ds.value + ds.offset)
        self.assertEqual(ds.get_value(use_offset=False), ds.value)


if __name__ == '__main__':
    unittest.main()
