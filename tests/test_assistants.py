import unittest

from nextnanopy.nnp.assistants import InputAssistant


class TestPoint(unittest.TestCase):
    def setUp(self):
        self.ia = InputAssistant()

    def test_point_wraps_values_in_brackets(self):
        self.assertEqual(self.ia.point("range_y", 0, 10), "range_y = [0, 10]")

    def test_point_accepts_any_number_of_values(self):
        self.assertEqual(self.ia.point("pos", 1, 2, 3), "pos = [1, 2, 3]")


class TestOutputSection(unittest.TestCase):
    def setUp(self):
        self.ia = InputAssistant()

    def test_coords_are_emitted(self):
        out = self.ia.output_section("my_section", dim=2, x=5)
        self.assertIn("name = my_section", out)
        self.assertIn("x = 5", out)
        self.assertTrue(out.startswith("section2D{"))

    def test_ranges_are_emitted(self):
        """range_* used to be silently dropped: the loop iterated an empty dict."""
        out = self.ia.output_section("s", dim=2, x=5, range_y=[0, 10], range_z=[0, 3])
        self.assertIn("range_y = [0, 10]", out)
        self.assertIn("range_z = [0, 3]", out)

    def test_ranges_accept_tuple_or_list(self):
        as_list = self.ia.output_section("s", dim=2, x=5, range_y=[0, 10])
        as_tuple = self.ia.output_section("s", dim=2, x=5, range_y=(0, 10))
        self.assertEqual(as_list, as_tuple)

    def test_range_values_are_unpacked_not_stringified(self):
        """point(key, value) would emit 'range_y = [(0, 10)]'; point(key, *value) is correct."""
        out = self.ia.output_section("s", dim=2, x=5, range_y=(0, 10))
        self.assertIn("range_y = [0, 10]", out)
        self.assertNotIn("(0, 10)", out)

    def test_omitted_ranges_are_absent(self):
        out = self.ia.output_section("s", dim=2, x=5)
        for key in ("range_x", "range_y", "range_z"):
            self.assertNotIn(key, out)

    def test_all_three_ranges(self):
        out = self.ia.output_section(
            "cut", dim=1, x=1, y=2, range_x=[0, 1], range_y=[0, 2], range_z=[0, 3]
        )
        self.assertIn("range_x = [0, 1]", out)
        self.assertIn("range_y = [0, 2]", out)
        self.assertIn("range_z = [0, 3]", out)
        self.assertTrue(out.startswith("section1D{"))

    def test_dim_selects_block_name(self):
        self.assertTrue(self.ia.output_section("s", dim=3, x=1).startswith("section3D{"))


if __name__ == "__main__":
    unittest.main()
