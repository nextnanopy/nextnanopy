import unittest
from nextnanopy.utils.misc import *


class TestMisc(unittest.TestCase):
    def test_find_name_max_idx(self):
        self.assertEqual(find_unused_name('ex.in', [''], extension='.in', max_idx=True), 'ex_0.in')
        self.assertEqual(find_unused_name('ex.in', ['ex_0.in'], extension='.in', max_idx=True), 'ex_1.in')
        self.assertEqual(find_unused_name('ex.in', ['ex_0.in', 'ex_1.in'], extension='.in', max_idx=True), 'ex_2.in')
        self.assertEqual(find_unused_name('ex.in', ['ex_0.in', 'ex_2.in'], extension='.in', max_idx=True), 'ex_3.in')
        self.assertEqual(find_unused_name('ex.in', ['ex_0.in', 'ex_2.in'], extension='.txt', max_idx=True),
                         'ex.in_0.txt')
        self.assertEqual(find_unused_name('ex.in', ['ex_0.txt', 'ex_2.txt'], extension='.in', max_idx=True), 'ex_0.in')

        self.assertEqual(find_unused_name('ex_0.in', [''], extension='.in', max_idx=True), 'ex_0.in')
        self.assertEqual(find_unused_name('ex_0.in', ['ex_0.in'], extension='.in', max_idx=True), 'ex_1.in')
        self.assertEqual(find_unused_name('ex_0.in', ['ex_0.in', 'ex_1.in'], extension='.in', max_idx=True), 'ex_2.in')
        self.assertEqual(find_unused_name('ex_0.in', ['ex_0.in', 'ex_2.in'], extension='.in', max_idx=True), 'ex_3.in')
        self.assertEqual(find_unused_name('ex_0.in', ['ex_0.in', 'ex_2.in'], extension='.txt', max_idx=True),
                         'ex_0.txt')
        self.assertEqual(find_unused_name('ex_0.in', ['ex_0.txt', 'ex_2.txt'], extension='.in', max_idx=True),
                         'ex_0.in')

        self.assertEqual(find_unused_name('ex_0d_0.in', ['ex_0d_0.in'], extension='.in', max_idx=True), 'ex_0d_1.in')
        self.assertEqual(find_unused_name('ex_0d_0.in', ['ex_0d_0.in', 'ex_0d_2.in'], extension='.in', max_idx=True),
                         'ex_0d_3.in')

    def test_find_name_min_idx(self):
        self.assertEqual(find_unused_name('ex.in', [''], extension='.in', max_idx=False), 'ex_0.in')
        self.assertEqual(find_unused_name('ex.in', ['ex_0.in'], extension='.in', max_idx=False), 'ex_1.in')
        self.assertEqual(find_unused_name('ex.in', ['ex_0.in', 'ex_1.in'], extension='.in', max_idx=False), 'ex_2.in')
        self.assertEqual(find_unused_name('ex.in', ['ex_0.in', 'ex_2.in'], extension='.in', max_idx=False), 'ex_1.in')
        self.assertEqual(find_unused_name('ex.in', ['ex_0.in', 'ex_2.in'], extension='.txt', max_idx=False),
                         'ex.in_0.txt')
        self.assertEqual(find_unused_name('ex.in', ['ex_0.txt', 'ex_2.txt'], extension='.in', max_idx=False), 'ex_0.in')
        self.assertEqual(find_unused_name('ex.in', ['ex_0.txt', 'ex_2.in'], extension='.in', max_idx=False), 'ex_0.in')

        self.assertEqual(find_unused_name('ex_0.in', [''], extension='.in', max_idx=False), 'ex_0.in')
        self.assertEqual(find_unused_name('ex_0.in', ['ex_0.in'], extension='.in', max_idx=False), 'ex_1.in')
        self.assertEqual(find_unused_name('ex_0.in', ['ex_0.in', 'ex_1.in'], extension='.in', max_idx=False), 'ex_2.in')
        self.assertEqual(find_unused_name('ex_0.in', ['ex_0.in', 'ex_2.in'], extension='.in', max_idx=False), 'ex_1.in')
        self.assertEqual(find_unused_name('ex_0.in', ['ex_0.in', 'ex_2.in'], extension='.txt', max_idx=False),
                         'ex_0.txt')
        self.assertEqual(find_unused_name('ex_0.in', ['ex_0.txt', 'ex_2.txt'], extension='.in', max_idx=False),
                         'ex_0.in')
        self.assertEqual(find_unused_name('ex_0d_0.in', ['ex_0d_0.in'], extension='.in', max_idx=False), 'ex_0d_1.in')
        self.assertEqual(find_unused_name('ex_0d_0.in', ['ex_0d_0.in', 'ex_0d_2.in'], extension='.in', max_idx=False),
                         'ex_0d_1.in')

if __name__ == '__main__':
    unittest.main()
