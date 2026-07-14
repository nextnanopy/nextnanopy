import builtins
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from nextnanopy import defaults
from nextnanopy.negf import defaults as negf_defaults
from nextnanopy.nn3 import defaults as nn3_defaults
from nextnanopy.nnp import defaults as nnp_defaults
from nextnanopy.utils import mycollections

folder_nnp = Path("tests") / "datafiles" / "nextnano++"
folder_nn3 = Path("tests") / "datafiles" / "nextnano3"
folder_negf = Path("tests") / "datafiles" / "nextnano.NEGF"
folder_msb = Path("tests") / "datafiles" / "nextnano.MSB"


class TestDictlist(unittest.TestCase):
    def test_dictlist(self):
        a = mycollections.DictList(a=2, b=3, c=4)
        self.assertEqual(a[0], 2)
        self.assertEqual(a["a"], 2)
        self.assertEqual(a[1], 3)
        self.assertEqual(a["b"], 3)
        self.assertEqual(list(a.keys()), ["a", "b", "c"])
        self.assertEqual(list(a.values()), [2, 3, 4])


class TestFormatting(unittest.TestCase):
    def test_nn3(self):
        fullpath = folder_nn3 / "example.in"
        self.assertTrue(nn3_defaults.is_nn3_input_file(fullpath))
        self.assertFalse(nnp_defaults.is_nnp_input_file(fullpath))
        self.assertFalse(negf_defaults.is_negf_classic_input_file(fullpath))
        self.assertFalse(negf_defaults.is_negf_input_file(fullpath))
        self.assertEqual(defaults.input_file_type(fullpath), "nextnano3")
        self.assertEqual(defaults.get_fmt("nextnano3")["var_char"], "%")
        self.assertEqual(defaults.get_fmt("nextnano3")["com_char"], "!")
        self.assertEqual(
            defaults.get_fmt("nextnano3")["input_pattern"], "$end_simulation-dimension"
        )

    def test_nnp(self):
        fullpath = folder_nnp / "example.in"
        self.assertFalse(nn3_defaults.is_nn3_input_file(fullpath))
        self.assertTrue(nnp_defaults.is_nnp_input_file(fullpath))
        self.assertFalse(negf_defaults.is_negf_classic_input_file(fullpath))
        self.assertFalse(negf_defaults.is_negf_input_file(fullpath))
        self.assertEqual(defaults.input_file_type(fullpath), "nextnano++")
        self.assertEqual(defaults.get_fmt("nextnano++")["var_char"], "$")
        self.assertEqual(defaults.get_fmt("nextnano++")["com_char"], "#")
        self.assertEqual(defaults.get_fmt("nextnano++")["input_pattern"], "global{")

    def test_negf_classic(self):
        fullpath = folder_negf / "example.xml"
        self.assertFalse(nn3_defaults.is_nn3_input_file(fullpath))
        self.assertFalse(nnp_defaults.is_nnp_input_file(fullpath))
        self.assertFalse(negf_defaults.is_negf_input_file(fullpath))
        self.assertTrue(negf_defaults.is_negf_classic_input_file(fullpath))
        self.assertEqual(defaults.input_file_type(fullpath), "nextnano.NEGF_classic")
        self.assertEqual(defaults.get_fmt("nextnano.NEGF_classic")["var_char"], "$")
        self.assertEqual(defaults.get_fmt("nextnano.NEGF_classic")["com_char"], "<!--")
        self.assertEqual(defaults.get_fmt("nextnano.NEGF_classic")["input_pattern"], "<Simulation")

    def test_negf(self):
        fullpath = folder_negf / "Minimal_InputFile.negf"
        self.assertFalse(nn3_defaults.is_nn3_input_file(fullpath))
        self.assertFalse(nnp_defaults.is_nnp_input_file(fullpath))
        self.assertFalse(negf_defaults.is_negf_classic_input_file(fullpath))
        self.assertTrue(negf_defaults.is_negf_input_file(fullpath))
        self.assertEqual(defaults.input_file_type(fullpath), "nextnano.NEGF")
        self.assertEqual(defaults.get_fmt("nextnano.NEGF")["var_char"], "$")
        self.assertEqual(defaults.get_fmt("nextnano.NEGF")["com_char"], "#")
        self.assertEqual(defaults.get_fmt("nextnano.NEGF")["input_pattern"], "nextnano.NEGF{")


class TestInputFileType(unittest.TestCase):
    """input_file_type() reads the file once and delegates to input_text_type().

    The two used to be parallel if/elif chains over the same five patterns -- one
    reopening the file per probe, one working on a string. They must agree.
    """

    def test_agrees_with_input_text_type(self):
        for fullpath in [
            folder_nn3 / "example.in",
            folder_nnp / "example.in",
            folder_negf / "example.xml",
            folder_negf / "Minimal_InputFile.negf",
            folder_msb / "example.xml",
        ]:
            with self.subTest(fullpath=fullpath):
                text = Path(fullpath).read_text()
                self.assertEqual(
                    defaults.input_file_type(fullpath),
                    defaults.input_text_type(text),
                )

    def test_unrecognized_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            fullpath = Path(tmp) / "junk.in"
            fullpath.write_text("this is not a nextnano input file\n")
            self.assertEqual(defaults.input_file_type(fullpath), "not valid")

    def test_reads_the_file_once(self):
        # the whole point of the change: detection is one open(), not one per product.
        # A file matching no product used to be the worst case -- all five probes ran.
        fullpath = folder_nnp / "example.in"
        real_open = builtins.open
        opened = []

        def counting_open(file, *args, **kwargs):
            opened.append(file)
            return real_open(file, *args, **kwargs)

        with mock.patch("builtins.open", counting_open):
            product = defaults.input_file_type(fullpath)

        self.assertEqual(product, "nextnano++")
        self.assertEqual(len(opened), 1)


if __name__ == "__main__":
    unittest.main()
