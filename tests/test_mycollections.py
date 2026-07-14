import unittest

from nextnanopy.utils.mycollections import DictList


class TestDictList(unittest.TestCase):
    def test_indexes(self):
        dl = DictList(a=3, b="test")
        self.assertEqual(list(dl.keys())[0], "a")
        self.assertEqual(list(dl.keys())[1], "b")
        self.assertEqual(list(dl.values())[0], 3)
        self.assertEqual(list(dl.values())[1], "test")
        self.assertEqual(dl[0], dl["a"])
        self.assertEqual(dl[0], 3)
        self.assertEqual(dl[1], dl["b"])
        self.assertEqual(dl[1], "test")

    def test_loop(self):
        dl = DictList(a=3, b="test")
        for value, expected in zip(dl, dl.values(), strict=True):
            self.assertEqual(value, expected)

    def test_nested_loops_are_independent(self):
        dl = DictList(a=3, b="test")
        pairs = [(outer, inner) for outer in dl for inner in dl]
        self.assertEqual(pairs, [(3, 3), (3, "test"), ("test", 3), ("test", "test")])

    def test_dict_semantics_are_key_based(self):
        dl = DictList(a=3, b="test")
        self.assertEqual(dict(dl), {"a": 3, "b": "test"})
        self.assertIn("a", dl)
        self.assertNotIn(3, dl)
        other = DictList()
        other.update(dl)
        self.assertEqual(list(other.items()), [("a", 3), ("b", "test")])


if __name__ == "__main__":
    unittest.main()
