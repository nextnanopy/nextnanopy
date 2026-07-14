import itertools
import os
import tempfile
import unittest
from pathlib import Path

from nextnanopy.utils.misc import candidate_names, savetxt


class TestCandidateNames(unittest.TestCase):
    """candidate_names yields the paths savetxt tries, in order: the requested name first,
    then name_0, name_1, ... It is an infinite generator and touches no filesystem - which
    of the candidates is actually free is savetxt's problem, not its own."""

    def candidates(self, name, n=4):
        return [p.name for p in itertools.islice(candidate_names(Path(name)), n)]

    def test_requested_name_comes_first_then_indices(self):
        self.assertEqual(self.candidates("ex.in"), ["ex.in", "ex_0.in", "ex_1.in", "ex_2.in"])

    def test_an_index_on_the_name_is_dropped_before_counting(self):
        # 'ex_0.in' must fall back to 'ex_1.in', not to 'ex_0_0.in'
        self.assertEqual(self.candidates("ex_0.in"), ["ex_0.in", "ex_0.in", "ex_1.in", "ex_2.in"])

    def test_only_the_trailing_index_is_dropped(self):
        self.assertEqual(
            self.candidates("ex_0d_0.in"),
            ["ex_0d_0.in", "ex_0d_0.in", "ex_0d_1.in", "ex_0d_2.in"],
        )

    def test_a_non_numeric_tail_is_not_an_index(self):
        self.assertEqual(
            self.candidates("ex_abc.in"),
            ["ex_abc.in", "ex_abc_0.in", "ex_abc_1.in", "ex_abc_2.in"],
        )

    def test_a_missing_suffix_needs_no_special_case(self):
        self.assertEqual(
            self.candidates("Makefile"), ["Makefile", "Makefile_0", "Makefile_1", "Makefile_2"]
        )

    def test_the_suffix_is_preserved_verbatim(self):
        self.assertEqual(self.candidates("ex.info", n=2), ["ex.info", "ex_0.info"])

    def test_the_folder_is_preserved(self):
        candidates = itertools.islice(candidate_names(Path("out") / "sub" / "ex.in"), 2)
        self.assertEqual(
            [str(p) for p in candidates],
            [os.path.join("out", "sub", "ex.in"), os.path.join("out", "sub", "ex_0.in")],
        )


class TestSavetxt(unittest.TestCase):
    """Contract of savetxt.

    1. If the requested name is free, it is used as-is - no index is appended.
    2. Otherwise the first free index is taken, filling any gaps.
    3. Siblings are matched on exact stem + suffix, never as substrings.

    Every test also checks the file it was told about really exists and holds the text, and
    that no stray file was left behind.
    """

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.folder = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def touch(self, *names):
        for name in names:
            (self.folder / name).write_text("")

    def save(self, name, text="x", **kwargs):
        """savetxt, asserting it really wrote the file whose path it returned."""
        out = Path(savetxt(str(self.folder / name), text, **kwargs))
        self.assertTrue(out.is_file(), f"savetxt returned {out}, but no such file exists")
        self.assertEqual(out.read_text(), text, f"{out} does not hold the text that was saved")
        return out

    def assertFolderHolds(self, *names):
        """The folder contains exactly these files - savetxt created no strays."""
        self.assertEqual(sorted(p.name for p in self.folder.iterdir()), sorted(names))

    # --- rule 1: a free name is used unchanged ---------------------------------

    def test_free_name_is_saved_without_an_index(self):
        out = self.save("ex.in", "hello")
        self.assertEqual(out.name, "ex.in")
        self.assertEqual(out.parent, self.folder)
        self.assertFolderHolds("ex.in")

    def test_free_name_wins_even_if_indexed_siblings_exist(self):
        self.touch("ex_0.in", "ex_1.in")
        self.assertEqual(self.save("ex.in").name, "ex.in")
        self.assertFolderHolds("ex.in", "ex_0.in", "ex_1.in")

    def test_free_indexed_name_is_saved_unchanged(self):
        self.assertEqual(self.save("ex_0.in").name, "ex_0.in")
        self.assertFolderHolds("ex_0.in")

    # --- rule 2: taken name -> first free index, gaps included -----------------

    def test_taken_name_falls_back_to_index_0(self):
        self.touch("ex.in")
        self.assertEqual(self.save("ex.in").name, "ex_0.in")
        self.assertFolderHolds("ex.in", "ex_0.in")

    def test_repeated_saves_walk_up_the_indices(self):
        names = [self.save("ex.in", str(i)).name for i in range(3)]
        self.assertEqual(names, ["ex.in", "ex_0.in", "ex_1.in"])
        self.assertFolderHolds("ex.in", "ex_0.in", "ex_1.in")
        # each save landed in its own file, none of them clobbered an earlier one
        self.assertEqual([(self.folder / n).read_text() for n in names], ["0", "1", "2"])

    def test_gap_in_the_indices_is_reused(self):
        self.touch("ex.in", "ex_0.in", "ex_2.in")
        self.assertEqual(self.save("ex.in").name, "ex_1.in")
        self.assertFolderHolds("ex.in", "ex_0.in", "ex_1.in", "ex_2.in")

    def test_taken_indexed_name_moves_to_the_next_free_index(self):
        self.touch("ex_0.in")
        self.assertEqual(self.save("ex_0.in").name, "ex_1.in")
        self.assertFolderHolds("ex_0.in", "ex_1.in")

    # --- rule 3: siblings match on exact stem + suffix -------------------------

    def test_a_longer_stem_is_not_a_sibling(self):
        # 'ex' is a substring of 'complex_0', but complex_0.in is a different file
        self.touch("ex.in", "complex_0.in", "complex_1.in")
        self.assertEqual(self.save("ex.in").name, "ex_0.in")
        self.assertFolderHolds("ex.in", "ex_0.in", "complex_0.in", "complex_1.in")

    def test_a_longer_suffix_is_not_a_sibling(self):
        # '.in' is a substring of '.input', but ex_0.input is a different file
        self.touch("ex.in", "ex_0.input", "ex_1.input")
        self.assertEqual(self.save("ex.in").name, "ex_0.in")
        self.assertFolderHolds("ex.in", "ex_0.in", "ex_0.input", "ex_1.input")

    def test_a_different_suffix_is_not_a_sibling(self):
        self.touch("ex.in", "ex_0.txt", "ex_1.txt")
        self.assertEqual(self.save("ex.in").name, "ex_0.in")
        self.assertFolderHolds("ex.in", "ex_0.in", "ex_0.txt", "ex_1.txt")

    def test_the_requested_suffix_is_never_rewritten(self):
        out = self.save("ex.info")
        self.assertEqual(out.suffix, ".info")
        self.assertFolderHolds("ex.info")

    # --- extensionless targets --------------------------------------------------

    def test_extensionless_free_name_is_saved_unchanged(self):
        self.assertEqual(self.save("Makefile").name, "Makefile")
        self.assertFolderHolds("Makefile")

    def test_extensionless_taken_name_gets_an_index(self):
        self.touch("input")
        self.assertEqual(self.save("input").name, "input_0")
        self.assertFolderHolds("input", "input_0")

    # --- overwrite / mkdir / return value --------------------------------------

    def test_overwrite_writes_the_exact_path(self):
        self.touch("ex.in")
        out = self.save("ex.in", "new", overwrite=True)
        self.assertEqual(out, self.folder / "ex.in")
        self.assertFolderHolds("ex.in")  # no ex_0.in stray

    def test_automkdir_creates_missing_parents(self):
        out = self.save(Path("a") / "b" / "ex.in", automkdir=True)
        self.assertEqual(out.name, "ex.in")
        self.assertEqual(out.parent, self.folder / "a" / "b")
        self.assertFolderHolds("a")

    def test_missing_folder_without_automkdir_raises(self):
        target = str(self.folder / "missing" / "ex.in")
        self.assertRaises(FileNotFoundError, savetxt, target, "x", automkdir=False)
        self.assertFolderHolds()  # nothing was created on the way to the error

    def test_returns_path_of_the_file_actually_written(self):
        out = savetxt(str(self.folder / "ex.in"), "x")
        self.assertIsInstance(out, str)
        self.assertTrue(os.path.isfile(out))


if __name__ == "__main__":
    unittest.main()
