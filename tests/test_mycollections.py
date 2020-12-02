import unittest
from nextnanopy.utils.mycollections import DictList


class TestDictList(unittest.TestCase):

    def test_indexes(self):
        dl = DictList(a=3, b='test')
        self.assertEqual(list(dl.keys())[0], 'a')
        self.assertEqual(list(dl.keys())[1], 'b')
        self.assertEqual(list(dl.values())[0], 3)
        self.assertEqual(list(dl.values())[1], 'test')
        self.assertEqual(dl[0], dl['a'])
        self.assertEqual(dl[0], 3)
        self.assertEqual(dl[1], dl['b'])
        self.assertEqual(dl[1], 'test')

    def test_loop(self):
        dl = DictList(a=3, b='test')
        for value, expected in zip(dl, dl.values()):
            self.assertEqual(value, expected)


if __name__ == '__main__':
    unittest.main()
