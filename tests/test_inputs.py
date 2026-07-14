import builtins
import os
import tempfile
import unittest
import unittest.mock
from pathlib import Path

from nextnanopy import defaults
from nextnanopy.inputs import InputFile, InputFileTemplate, Sweep
from nextnanopy.nnp.inputs import Parser


def delete_files(start, directory=None, exceptions=None):
    if directory is None:
        directory = Path.cwd()
    for fpath in Path(directory).iterdir():
        if fpath.name.startswith(start):
            if exceptions:
                if fpath.name in exceptions:
                    continue
                else:
                    fpath.unlink()
            else:
                fpath.unlink()


folder_nnp = Path("tests") / "datafiles" / "nextnano++"
folder_nn3 = Path("tests") / "datafiles" / "nextnano3"
folder_negf = Path("tests") / "datafiles" / "nextnano.NEGF"
folder_msb = Path("tests") / "datafiles" / "nextnano.MSB"


class Test_nnp(unittest.TestCase):
    def test_load(self):
        fullpath = folder_nnp / "only_variables.in"

        file = InputFile(fullpath)
        self.assertEqual(file.product, "nextnano++")

        self.assertEqual(len(file.variables.keys()), 7)
        self.assertEqual(file.variables["float"].name, "float")
        self.assertEqual(file.variables["float"].value, 0.0)
        self.assertEqual(file.variables["float"].comment, "float number (a.u.)")

        self.assertEqual(file.variables["int"].name, "int")
        self.assertEqual(file.variables["int"].value, 0)
        self.assertEqual(file.variables["int"].comment, "int number (random = 3)")

        self.assertEqual(file.variables["str"].name, "str")
        self.assertEqual(file.variables["str"].value, '"test"')
        self.assertEqual(file.variables["str"].comment, "first comments # second comment")

        self.assertEqual(file.variables["reference"].name, "reference")
        self.assertEqual(file.variables["reference"].value, "$int - 1")

        self.assertEqual(file.variables["NoSpacing"].name, "NoSpacing")
        self.assertEqual(file.variables["NoSpacing"].value, int("7"))
        self.assertEqual(file.variables["NoSpacing"].comment, "this is a comment")
        self.assertEqual(file.variables["NoSpacing"].text, "$NoSpacing = 7 # this is a comment")

        self.assertEqual(file.variables["MAYUS"].name, "MAYUS")
        self.assertEqual(file.variables["MAYUS"].value, "TEXT")
        self.assertEqual(file.variables["MAYUS"].comment, "")
        self.assertEqual(file.variables["MAYUS"].text, "$MAYUS = TEXT")

        fullpath = folder_nnp / "virtual_file.in"
        self.assertRaises(FileNotFoundError, InputFile, fullpath)

    def test_get_variables(self):
        fullpath = folder_nn3 / "only_variables.in"
        file = InputFile(fullpath)

        self.assertEqual(file.variables["float"], file.get_variable("float"))
        self.assertRaises(KeyError, file.get_variable, name="new_variable")

    def test_set_variables(self):
        fullpath = folder_nnp / "only_variables.in"
        file = InputFile(fullpath)
        file.set_variable("float", 1e-5, "some comment", "some unit")  # unit is not visible in nn++

        self.assertEqual(file.variables["float"].name, "float")
        self.assertEqual(file.variables["float"].value, 1e-5)
        self.assertEqual(file.variables["float"].comment, "some comment")
        self.assertEqual(file.variables["float"].text, f"$float = {str(1e-5)} # some comment")
        self.assertEqual(file.lines[3], f"$float = {str(1e-5)} # some comment")

        file.set_variable("float", value=1e-7)
        self.assertEqual(file.variables["float"].name, "float")
        self.assertEqual(file.variables["float"].value, 1e-7)
        self.assertEqual(file.variables["float"].comment, "some comment")
        self.assertEqual(file.variables["float"].text, f"$float = {str(1e-7)} # some comment")
        self.assertEqual(file.lines[3], f"$float = {str(1e-7)} # some comment")

        file.set_variable("float", comment="new comment")
        self.assertEqual(file.variables["float"].name, "float")
        self.assertEqual(file.variables["float"].value, 1e-7)
        self.assertEqual(file.variables["float"].comment, "new comment")
        self.assertEqual(file.variables["float"].text, f"$float = {str(1e-7)} # new comment")
        self.assertEqual(file.lines[3], f"$float = {str(1e-7)} # new comment")

        file.set_variable("float", value=0)
        self.assertEqual(file.variables["float"].value, 0)
        file.set_variable("float", value="0")
        self.assertEqual(file.variables["float"].value, "0")
        self.assertRaises(KeyError, file.set_variable, name="new_variable")
        self.assertRaises(KeyError, file.set_variable, name="new_variable")

    def test_fullpath(self):
        fullpath = folder_nnp / "only_variables.in"
        file = InputFile(fullpath)

        self.assertEqual(Path(file.fullpath), fullpath)
        self.assertEqual(
            Path(file.save(file.fullpath, overwrite=False)),
            folder_nnp / "only_variables_0.in",
        )
        Path(file.fullpath).unlink()

    def test_config(self):
        fullpath = folder_nnp / "only_variables.in"
        file = InputFile(fullpath)
        from nextnanopy import config

        for key, value in config.config["nextnano++"].items():
            self.assertEqual(file.default_command_args[key], value)

    def test_text(self):
        fullpath_onlyvar = folder_nnp / "only_variables.in"
        fullpath_example = folder_nnp / "example.in"
        file = InputFile(fullpath_onlyvar)
        text = file.text

        new_file = InputFile(fullpath_example)
        new_file.text = text
        self.assertEqual(new_file.product, "nextnano++")
        self.assertEqual(new_file.text, text)
        self.assertEqual(new_file.lines, file.lines)
        self.assertEqual(new_file.variables["MAYUS"].name, "MAYUS")
        self.assertEqual(new_file.variables["MAYUS"].value, "TEXT")
        self.assertEqual(new_file.variables["MAYUS"].comment, "")
        self.assertEqual(new_file.variables["MAYUS"].text, "$MAYUS = TEXT")
        self.assertEqual(
            Path(new_file.save(file.fullpath, overwrite=False)),
            folder_nnp / "only_variables_0.in",
        )
        Path(new_file.fullpath).unlink()

    def test_set_and_save(self):
        fullpath = folder_nnp / "only_variables.in"
        file = InputFile(fullpath)
        file.set_variable(name="float", value=0.4)
        self.assertAlmostEqual(file.variables["float"].value, 0.4)

        self.addCleanup((folder_nnp / "only_variables_0.in").unlink)
        file.save()
        self.assertTrue((folder_nnp / "only_variables_0.in").is_file())

    def test_save_temp(self):
        # The saved filename is deliberately not asserted here. _get_temp_dir hands out one
        # directory per class for the whole process, so an earlier temp save of the same file
        # (Sweep.save_sweep does one) is still sitting in it and pushes this save onto an
        # index - which index depends on test order. test_save_to_another_folder covers the
        # "free name keeps its name" contract in a directory this test owns.
        fullpath = folder_nnp / "only_variables.in"
        file = InputFile(fullpath)
        file.save(temp=True)
        self.assertTrue(Path(file.fullpath).is_file())
        try:
            self.assertTrue(Path(file.fullpath).is_file())
            # Check that the file is in the system temp directory
            temp_dir = Path(tempfile.gettempdir()).resolve()
            file_dir = Path(file.fullpath).resolve().parent
            self.assertTrue(str(file_dir).startswith(str(temp_dir)))
        finally:
            if Path(file.fullpath).exists():
                Path(file.fullpath).unlink()

    def test_save_to_another_folder(self):
        file = InputFile(folder_nnp / "only_variables.in")
        with tempfile.TemporaryDirectory() as target:
            target = Path(target)

            # the name is free in the target folder, so it is kept as-is
            first = Path(file.save(target / "only_variables.in"))
            self.assertEqual(first.name, "only_variables.in")
            self.assertTrue(first.is_file())
            self.assertEqual([p.name for p in target.iterdir()], ["only_variables.in"])

            # only once the name is taken does an index appear
            second = Path(file.save(target / "only_variables.in"))
            self.assertEqual(second.name, "only_variables_0.in")
            self.assertTrue(second.is_file())

            # the source file in the original folder was left alone
            self.assertFalse((folder_nnp / "only_variables_0.in").exists())

    def test_same_dir_saving(self):
        current_directory = Path.cwd()
        self.addCleanup(os.chdir, current_directory)

        os.chdir(folder_nnp)

        path = "only_variables.in"
        file = InputFile(path)
        file.set_variable(name="float", value=0.3333)
        self.assertAlmostEqual(file.variables["float"].value, 0.3333)
        self.addCleanup(
            delete_files,
            "only_variables",
            directory=".",
            exceptions=["only_variables.in"],
        )
        file.save()
        self.assertTrue(Path("only_variables_0.in").is_file())

    ###content tests

    def test_content_get(self):
        fullpath = folder_nnp / "only_variables.in"
        file = InputFile(fullpath, parse=True)

        self.assertIsNotNone(file.content)
        self.assertEqual(file.content[0], "$float = 0.0 ")
        self.assertEqual(file.content[-1].name, "global")

    def test_content_set(self):
        fullpath = folder_nnp / "only_variables.in"
        file = InputFile(fullpath, parse=True)

        file.content[0] = "$DUMMY = 1"
        self.assertEqual(file.content[0], "$DUMMY = 1")
        file.content["_entry_0"] = "DUMMY LINE"
        self.assertEqual(file.content[0], "DUMMY LINE")

    def test_content_roundtrip_does_not_duplicate_statements(self):
        """A block written on one line must not leak its body into the enclosing blocks.

        Compare against the *original* text, not against a second parse: re-parsing the
        duplicated output is idempotent, so a parse-twice-and-compare check passes even
        when the tree is corrupt.
        """
        fullpath = folder_nnp / "example.in"
        file = InputFile(fullpath, parse=True)
        rendered = str(file.content)

        for statement in ['pos =', 'spacing =', 'name = "GaAs"', "num_ev =", "alloy_x ="]:
            self.assertEqual(
                rendered.count(statement),
                file.raw_text.count(statement),
                f"{statement!r} was duplicated by the parser",
            )

    def test_content_roundtrip_preserves_block_nesting(self):
        parser = Parser()
        parser.parse("global{ sub{ a = 1 } }", mode="str")

        outer = parser.result.content[0]
        inner = outer.content[0]
        self.assertEqual(len(parser.result.content), 1)  # nothing leaked to the root
        self.assertEqual(len(outer.content), 1)  # nothing leaked into global{}
        self.assertEqual(inner.content, ["a = 1 "])

    def test_non_parseable_parse_true_raises(self):
        fullpath = folder_nnp / "example_non_parseable.nnp"
        with self.assertRaises(ValueError):
            InputFile(fullpath, parse=True)

    def test_non_parseable_parse_false_ok(self):
        fullpath = folder_nnp / "example_non_parseable.nnp"
        file = InputFile(fullpath, parse=False)
        self.assertIsNone(file.content)
        self.assertEqual(len(file.variables), 8)
        self.assertAlmostEqual(file.variables["BIAS"].value, 0.0)
        self.assertAlmostEqual(file.variables["ALLOY"].value, 0.3)


class Test_nn3(unittest.TestCase):
    def test_load(self):
        fullpath = folder_nn3 / "only_variables.in"

        file = InputFile(fullpath)
        self.assertEqual(file.product, "nextnano3")

        self.assertEqual(len(file.variables.keys()), 7)
        self.assertEqual(file.variables["float"].name, "float")
        self.assertEqual(file.variables["float"].value, 0.0)
        self.assertEqual(file.variables["float"].comment, "float number (a.u.)")

        self.assertEqual(file.variables["int"].name, "int")
        self.assertEqual(file.variables["int"].value, 0)
        self.assertEqual(file.variables["int"].comment, "int number (random = 3)")

        self.assertEqual(file.variables["str"].name, "str")
        self.assertEqual(file.variables["str"].value, '"test"')
        self.assertEqual(file.variables["str"].comment, "first comments # second comment")

        self.assertEqual(file.variables["reference"].name, "reference")
        self.assertEqual(file.variables["reference"].value, "$int - 1")

        self.assertEqual(file.variables["NoSpacing"].name, "NoSpacing")
        self.assertEqual(file.variables["NoSpacing"].value, int("7"))
        self.assertEqual(file.variables["NoSpacing"].comment, "this is a comment")

        self.assertEqual(file.variables["MAYUS"].name, "MAYUS")
        self.assertEqual(file.variables["MAYUS"].value, "TEXT")
        self.assertEqual(file.variables["MAYUS"].comment, "")

        fullpath = folder_nn3 / "virtual_file.in"
        self.assertRaises(FileNotFoundError, InputFile, fullpath)

    def test_get_variables(self):
        fullpath = folder_nn3 / "only_variables.in"
        file = InputFile(fullpath)

        self.assertEqual(file.variables["float"], file.get_variable("float"))
        self.assertRaises(KeyError, file.get_variable, name="new_variable")

    def test_set_variables(self):
        fullpath = folder_nn3 / "only_variables.in"
        file = InputFile(fullpath)
        file.set_variable("float", 1e-5, "some comment")

        self.assertEqual(file.variables["float"].name, "float")
        self.assertEqual(file.variables["float"].value, 1e-5)
        self.assertEqual(file.variables["float"].comment, "some comment")
        self.assertEqual(file.variables["float"].text, f"%float = {str(1e-5)} ! some comment")
        self.assertEqual(file.lines[3], f"%float = {str(1e-5)} ! some comment")

        file.set_variable("float", value=1e-7)
        self.assertEqual(file.variables["float"].name, "float")
        self.assertEqual(file.variables["float"].value, 1e-7)
        self.assertEqual(file.variables["float"].comment, "some comment")
        self.assertEqual(file.variables["float"].text, f"%float = {str(1e-7)} ! some comment")
        self.assertEqual(file.lines[3], f"%float = {str(1e-7)} ! some comment")

        file.set_variable("float", comment="new comment")
        self.assertEqual(file.variables["float"].name, "float")
        self.assertEqual(file.variables["float"].value, 1e-7)
        self.assertEqual(file.variables["float"].comment, "new comment")
        self.assertEqual(file.variables["float"].text, f"%float = {str(1e-7)} ! new comment")
        self.assertEqual(file.lines[3], f"%float = {str(1e-7)} ! new comment")

        file.set_variable("float", value=0)
        self.assertEqual(file.variables["float"].value, 0)
        file.set_variable("float", value="0")
        self.assertEqual(file.variables["float"].value, "0")
        self.assertRaises(KeyError, file.set_variable, name="new_variable")

    def test_fullpath(self):
        fullpath = folder_nn3 / "only_variables.in"
        file = InputFile(fullpath)

        self.assertEqual(Path(file.fullpath), fullpath)
        self.assertEqual(
            Path(file.save(file.fullpath, overwrite=False)),
            folder_nn3 / "only_variables_0.in",
        )
        Path(file.fullpath).unlink()

    def test_config(self):
        fullpath = folder_nn3 / "only_variables.in"
        file = InputFile(fullpath)
        from nextnanopy import config

        for key, value in config.config["nextnano3"].items():
            self.assertEqual(file.default_command_args[key], value)

    def test_save(self):
        fullpath = folder_nn3 / "only_variables.in"
        file = InputFile(fullpath)
        new_folder = folder_nn3 / "temp"
        new_file = new_folder / "example_copy.in"
        self.assertRaises(FileNotFoundError, file.save, new_file, overwrite=True, automkdir=False)
        self.assertEqual(Path(file.save(new_file, overwrite=True, automkdir=True)), new_file)
        Path(file.fullpath).unlink()
        new_folder.rmdir()

    def test_save_temp(self):
        fullpath = folder_nn3 / "only_variables.in"
        file = InputFile(fullpath)
        file.save(temp=True)
        self.assertTrue(Path(file.fullpath).is_file())
        try:
            self.assertTrue(Path(file.fullpath).is_file())
            # Check that the file is in the system temp directory
            temp_dir = Path(tempfile.gettempdir()).resolve()
            file_dir = Path(file.fullpath).resolve().parent
            self.assertTrue(str(file_dir).startswith(str(temp_dir)))
        finally:
            if Path(file.fullpath).exists():
                Path(file.fullpath).unlink()

    def test_text(self):
        fullpath_onlyvar = folder_nn3 / "only_variables.in"
        fullpath_example = folder_nn3 / "example.in"
        file = InputFile(fullpath_onlyvar)
        text = file.text

        new_file = InputFile(fullpath_example)
        new_file.text = text

        self.assertEqual(new_file.product, "nextnano3")
        self.assertEqual(new_file.text, text)
        self.assertEqual(new_file.lines, file.lines)
        self.assertEqual(new_file.variables["MAYUS"].name, "MAYUS")
        self.assertEqual(new_file.variables["MAYUS"].value, "TEXT")
        self.assertEqual(new_file.variables["MAYUS"].comment, "")
        self.assertEqual(new_file.variables["MAYUS"].text, "%MAYUS = TEXT")
        self.assertEqual(
            Path(new_file.save(file.fullpath, overwrite=False)),
            folder_nn3 / "only_variables_0.in",
        )
        Path(new_file.fullpath).unlink()

    def test_set_and_save(self):
        fullpath = folder_nn3 / "only_variables.in"
        file = InputFile(fullpath)
        file.set_variable(name="float", value=0.4)
        self.assertAlmostEqual(file.variables["float"].value, 0.4)

        self.addCleanup((folder_nn3 / "only_variables_0.in").unlink)
        file.save()
        self.assertTrue((folder_nn3 / "only_variables_0.in").is_file())

    def test_same_dir(self):
        current_directory = Path.cwd()
        self.addCleanup(os.chdir, current_directory)

        os.chdir(folder_nn3)

        path = "only_variables.in"
        file = InputFile(path)
        file.set_variable(name="float", value=0.3333)
        self.assertAlmostEqual(file.variables["float"].value, 0.3333)
        self.addCleanup(
            delete_files,
            "only_variables",
            directory=".",
            exceptions=["only_variables.in"],
        )
        file.save()
        self.assertTrue(Path("only_variables_0.in").is_file())

    def test_content(self):
        fullpath = folder_nn3 / "only_variables.in"
        file = InputFile(fullpath)

        self.assertIsNone(file.content)


class Test_negf_classic(unittest.TestCase):
    def test_load(self):
        fullpath = folder_negf / "example.xml"
        file = InputFile(fullpath)

        self.assertEqual(file.product, "nextnano.NEGF_classic")

        self.assertEqual(len(file.variables.keys()), 4)

        self.assertEqual(file.variables["variable1"].name, "variable1")
        self.assertEqual(file.variables["variable1"].value, 0.24)
        self.assertEqual(file.variables["variable1"].comment, "Some comment")
        self.assertEqual(file.variables["variable1"].unit, "")

        self.assertEqual(file.variables["variable2"].name, "variable2")
        self.assertEqual(file.variables["variable2"].value, 0)
        self.assertEqual(file.variables["variable2"].comment, "Another comment")
        self.assertEqual(file.variables["variable2"].unit, "meV")

        self.assertEqual(file.variables["text_var"].name, "text_var")
        self.assertEqual(file.variables["text_var"].value, "some text")

        self.assertEqual(file.variables["ref_var"].value, "$(1-variable1)")

        fullpath = folder_negf / "virtual_file.xml"
        self.assertRaises(FileNotFoundError, InputFile, fullpath)

    def test_get_variables(self):
        fullpath = folder_negf / "example.xml"
        file = InputFile(fullpath)

        self.assertEqual(file.variables["variable1"], file.get_variable("variable1"))

        self.assertRaises(KeyError, file.get_variable, name="new_variable")

    def test_set_variables(self):
        fullpath = folder_negf / "example.xml"
        file = InputFile(fullpath)

        file.set_variable("variable1", 0.137, "test comment", "test unit^2")
        self.assertEqual(file.variables["variable1"].value, 0.137)
        self.assertEqual(file.variables["variable1"].comment, "test comment")
        self.assertEqual(file.variables["variable1"].unit, "test unit^2")

        file.set_variable("text_var", "string variable test")
        self.assertEqual(file.variables["text_var"].value, "string variable test")

        file.set_variable("ref_var", "$variable1 - 0.1")
        self.assertEqual(file.variables["ref_var"].value, "$variable1 - 0.1")

        self.assertRaises(KeyError, file.set_variable, name="new_variable")

    def test_fullpath(self):
        fullpath = folder_negf / "example.xml"
        file = InputFile(fullpath)

        self.assertEqual(Path(file.fullpath), fullpath)
        self.assertEqual(
            Path(file.save(file.fullpath, overwrite=False)),
            folder_negf / "example_0.xml",
        )
        Path(file.fullpath).unlink()

    def test_config(self):
        fullpath = folder_negf / "example.xml"
        file = InputFile(fullpath)
        from nextnanopy import config

        for key, value in config.config["nextnano.NEGF_classic"].items():
            self.assertEqual(file.default_command_args[key], value)

    def test_save(self):
        fullpath = folder_negf / "example.xml"
        file = InputFile(fullpath)

        new_folder = folder_negf / "temp"
        new_file = new_folder / "example_copy.in"
        self.assertRaises(FileNotFoundError, file.save, new_file, overwrite=True, automkdir=False)
        self.assertEqual(Path(file.save(new_file, overwrite=True, automkdir=True)), new_file)
        Path(file.fullpath).unlink()
        new_folder.rmdir()

    def test_set_and_save(self):
        fullpath = folder_negf / "example.xml"
        file = InputFile(fullpath)
        file.set_variable(name="variable1", value=0.4)
        self.assertAlmostEqual(file.variables["variable1"].value, 0.4)

        self.addCleanup((folder_negf / "example_0.xml").unlink)
        file.save()
        self.assertTrue((folder_negf / "example_0.xml").is_file())

    def test_content(self):
        fullpath = folder_negf / "example.xml"
        file = InputFile(fullpath)

        self.assertIsNone(file.content)


class Test_negf_classic_variables_section(unittest.TestCase):
    """A <Variables> section must be read and written back correctly whether it
    is populated, present but empty, or absent altogether.

    These three shapes are the contract. The empty section is the interesting
    one: it exists but has no children, so any check that conflates "has
    children" with "was found" collapses it into the absent case.
    """

    def write_input(self, variables_section):
        text = (
            '<?xml version="1.0" encoding="utf-8"?>\n'
            "<Simulation>\n"
            f"{variables_section}"
            "</Simulation>\n"
        )
        fullpath = Path(tempfile.mkdtemp()) / "input.xml"
        fullpath.write_text(text)
        return fullpath

    def test_populated_variables_section(self):
        fullpath = self.write_input(
            "  <Variables>\n"
            '    <Constant><Name Comment="first">$alpha</Name>'
            '<Value Unit="nm">3.5</Value></Constant>\n'
            '    <Constant><Name Comment="second">$beta</Name>'
            '<Value Unit="meV">42</Value></Constant>\n'
            "  </Variables>\n"
        )
        file = InputFile(fullpath)

        self.assertEqual(len(file.variables.keys()), 2)
        self.assertEqual(file.variables["alpha"].value, 3.5)
        self.assertEqual(file.variables["alpha"].unit, "nm")
        self.assertEqual(file.variables["alpha"].comment, "first")
        self.assertEqual(file.variables["beta"].value, 42)

        # Edits must survive the round trip back out to XML.
        file.set_variable("alpha", value=7.5, unit="um", comment="edited")
        rendered = "\n".join(file.lines)
        self.assertIn('<Value Unit="um">7.5</Value>', rendered)
        self.assertIn('Comment="edited"', rendered)

    def test_empty_variables_section(self):
        fullpath = self.write_input("  <Variables></Variables>\n")
        file = InputFile(fullpath)

        # Present but childless: no variables, and the section is not dropped.
        self.assertEqual(len(file.variables.keys()), 0)
        self.assertIn("<Variables", "\n".join(file.lines))

    def test_missing_variables_section(self):
        fullpath = self.write_input("")
        file = InputFile(fullpath)

        self.assertEqual(len(file.variables.keys()), 0)
        self.assertNotIn("<Variables", "\n".join(file.lines))


class Test_negf(unittest.TestCase):
    # TODO: implement test for NEGF++ input file
    def test_load(self):
        fullpath = folder_negf / "Minimal_InputFile.negf"

        file = InputFile(fullpath)
        self.assertEqual(file.product, "nextnano.NEGF")

        self.assertEqual(len(file.variables.keys()), 1)
        self.assertEqual(file.variables["alloyComposition"].name, "alloyComposition")
        self.assertAlmostEqual(file.variables["alloyComposition"].value, 0.15, delta=1e-9)
        self.assertEqual(file.variables["alloyComposition"].comment, "alloy composition")

        fullpath = folder_nnp / "virtual_file.in"
        self.assertRaises(FileNotFoundError, InputFile, fullpath)

    def test_get_variables(self):
        fullpath = folder_negf / "Minimal_InputFile.negf"
        file = InputFile(fullpath)

        self.assertEqual(file.variables["alloyComposition"], file.get_variable("alloyComposition"))
        self.assertRaises(KeyError, file.get_variable, name="new_variable")

    def test_set_variables(self):
        fullpath = folder_negf / "Minimal_InputFile.negf"
        file = InputFile(fullpath)
        file.set_variable(
            "alloyComposition", 1e-5, "some comment", "some unit"
        )  # unit is not visible in nn++

        self.assertEqual(file.variables["alloyComposition"].name, "alloyComposition")
        self.assertEqual(file.variables["alloyComposition"].value, 1e-5)
        self.assertEqual(file.variables["alloyComposition"].comment, "some comment")
        self.assertEqual(
            file.variables["alloyComposition"].text,
            f"$alloyComposition = {str(1e-5)} # some comment",
        )
        self.assertEqual(file.lines[0], f"$alloyComposition = {str(1e-5)} # some comment")

        file.set_variable("alloyComposition", value=1e-7)
        self.assertEqual(file.variables["alloyComposition"].name, "alloyComposition")
        self.assertEqual(file.variables["alloyComposition"].value, 1e-7)
        self.assertEqual(file.variables["alloyComposition"].comment, "some comment")
        self.assertEqual(
            file.variables["alloyComposition"].text,
            f"$alloyComposition = {str(1e-7)} # some comment",
        )
        self.assertEqual(file.lines[0], f"$alloyComposition = {str(1e-7)} # some comment")

        file.set_variable("alloyComposition", comment="new comment")
        self.assertEqual(file.variables["alloyComposition"].name, "alloyComposition")
        self.assertEqual(file.variables["alloyComposition"].value, 1e-7)
        self.assertEqual(file.variables["alloyComposition"].comment, "new comment")
        self.assertEqual(
            file.variables["alloyComposition"].text,
            f"$alloyComposition = {str(1e-7)} # new comment",
        )
        self.assertEqual(file.lines[0], f"$alloyComposition = {str(1e-7)} # new comment")

        file.set_variable("alloyComposition", value=0)
        self.assertEqual(file.variables["alloyComposition"].value, 0)

        self.assertRaises(KeyError, file.set_variable, name="new_variable")
        self.assertRaises(KeyError, file.set_variable, name="new_variable")

    def test_fullpath(self):
        fullpath = folder_negf / "Minimal_InputFile.negf"
        file = InputFile(fullpath)

        self.assertEqual(Path(file.fullpath), fullpath)
        self.assertEqual(
            Path(file.save(file.fullpath, overwrite=False)),
            folder_negf / "Minimal_InputFile_0.negf",
        )
        Path(file.fullpath).unlink()

    def test_config(self):
        fullpath = folder_negf / "Minimal_InputFile.negf"
        file = InputFile(fullpath)
        from nextnanopy import config

        for key, value in config.config["nextnano.NEGF"].items():
            self.assertEqual(file.default_command_args[key], value)

    def test_set_and_save(self):
        fullpath = folder_negf / "Minimal_InputFile.negf"
        file = InputFile(fullpath)
        file.set_variable(name="alloyComposition", value=0.4)
        self.assertAlmostEqual(file.variables["alloyComposition"].value, 0.4)

        self.addCleanup((folder_negf / "Minimal_InputFile_0.negf").unlink)
        file.save()
        self.assertTrue((folder_negf / "Minimal_InputFile_0.negf").is_file())

    def test_same_dir_saving(self):
        current_directory = Path.cwd()
        self.addCleanup(os.chdir, current_directory)

        os.chdir(folder_negf)

        path = "Minimal_InputFile.negf"
        file = InputFile(path)
        file.set_variable(name="alloyComposition", value=0.3333)
        self.assertAlmostEqual(file.variables["alloyComposition"].value, 0.3333)
        self.addCleanup(
            delete_files,
            "Minimal_InputFile",
            directory=".",
            exceptions=["Minimal_InputFile.negf"],
        )
        file.save()
        self.assertTrue(Path("Minimal_InputFile_0.negf").is_file())


class Test_msb(unittest.TestCase):
    def test_load(self):
        fullpath = folder_msb / "example.msb"

        input_file = InputFile(fullpath)
        print(input_file)
        print(input_file.text)
        print(type(input_file))
        self.assertEqual(input_file.product, "nextnano.MSB")
        self.assertEqual(len(input_file.variables.keys()), 1)

        fullpath = folder_msb / "virtual_file.msb"
        self.assertRaises(FileNotFoundError, InputFile, fullpath)

    def get_variables(self):
        fullpath = folder_msb / "example.msb"
        input_file = InputFile(fullpath)

        self.assertEqual(
            input_file.variables["Well"],
            input_file.get_variable("Well"),
        )
        self.assertRaises(KeyError, input_file.get_variable, name="new_variable")

        self.assertEqual(input_file.variables["Well"].value, 0.14)

    def test_set_variable(self):
        fullpath = folder_msb / "example.msb"
        input_file = InputFile(fullpath)

        input_file.set_variable("Well", 0.2, "Updated well width", "nm")
        self.assertEqual(input_file.variables["Well"].value, 0.2)
        self.assertEqual(input_file.variables["Well"].comment, "Updated well width")
        self.assertEqual(input_file.variables["Well"].unit, "nm")

    def test_set_and_save(self):
        fullpath = folder_msb / "example.msb"
        input_file = InputFile(fullpath)

        input_file.set_variable(name="Well", value=0.25)
        self.assertAlmostEqual(input_file.variables["Well"].value, 0.25)
        self.addCleanup((folder_msb / "example_0.msb").unlink)
        input_file.save()
        self.assertTrue((folder_msb / "example_0.msb").is_file())
        input_file_1 = InputFile(folder_msb / "example_0.msb")
        self.assertAlmostEqual(input_file_1.variables["Well"].value, 0.25)


class TestInputFile(unittest.TestCase):
    def test_access_by_index(self):
        fullpath = folder_nnp / "only_variables.in"
        file = InputFile(fullpath)
        for key, value in file.variables.items():
            self.assertEqual(file[key], value)

    def test_for_loop(self):
        fullpath = folder_nnp / "only_variables.in"
        file = InputFile(fullpath)
        for i, fi in enumerate(file):
            self.assertEqual(file.variables[i], fi)

    def test_fullpath(self):
        fullpath = folder_nnp / "only_variables.in"
        file = InputFile(fullpath)
        self.assertEqual(Path(file.fullpath), fullpath)
        self.assertEqual(file.filename, "only_variables.in")
        self.assertEqual(file.filename_only, "only_variables")
        self.assertEqual(Path(file.folder_input), folder_nnp)
        self.assertEqual(file.execute_info, {})

        file.filename = "new_name.in"
        self.assertEqual(file.filename, "new_name.in")
        self.assertEqual(file.filename_only, "new_name")
        self.assertEqual(Path(file.fullpath), folder_nnp / "new_name.in")
        self.assertEqual(Path(file.folder_input), folder_nnp)

        file.filename_only = "another_filename"
        self.assertEqual(file.filename, "another_filename.in")
        self.assertEqual(file.filename_only, "another_filename")
        self.assertEqual(Path(file.fullpath), folder_nnp / "another_filename.in")
        self.assertEqual(Path(file.folder_input), folder_nnp)

        npath = Path("new") / "folder"
        file.folder_input = npath
        self.assertEqual(file.filename, "another_filename.in")
        self.assertEqual(file.filename_only, "another_filename")
        self.assertEqual(Path(file.fullpath), npath / "another_filename.in")
        self.assertEqual(Path(file.folder_input), npath)

        npath = Path("random") / "path"
        file.execute_info["outputdirectory"] = npath
        self.assertEqual(Path(file.folder_output), npath)


class TestNotValidProduct(unittest.TestCase):
    """The 'not valid' sentinel must be spelled the same everywhere.

    InputFileTemplate.validate() used to write 'Not valid' (capital N) while the
    __init__ default, both detectors (defaults.input_text_type / input_file_type) and
    the dispatch branch in defaults.get_InputFile all use lowercase 'not valid'. The
    mismatch made get_InputFile's 'not valid' -> InputFileTemplate branch unreachable,
    so loading any non-nextnano file raised `ValueError: Not valid is not valid`.
    """

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.fullpath = Path(self._tmp.name) / "junk.in"
        self.fullpath.write_text("this is not a nextnano input file\n")

    def tearDown(self):
        self._tmp.cleanup()

    def test_sentinel_is_lowercase_everywhere(self):
        # the sentinel the detectors emit, the dispatcher accepts, and validate() writes
        # must all be the same string.
        self.assertEqual(defaults.input_text_type("not a nextnano file"), "not valid")
        self.assertEqual(defaults.input_file_type(self.fullpath), "not valid")
        self.assertIs(defaults.get_InputFile("not valid"), InputFileTemplate)

        template = InputFileTemplate(self.fullpath)
        self.assertEqual(template.product, "not valid")

    def test_validate_keeps_the_lowercase_sentinel(self):
        # validate() is what rewrote the sentinel. Reach it directly: a fresh template
        # whose product is anything unrecognized must come out as lowercase 'not valid'.
        template = InputFileTemplate()
        template.product = "something unrecognized"
        template.validate()
        self.assertEqual(template.product, "not valid")

    def test_unrecognized_file_loads_as_template(self):
        # the user-visible consequence: this used to raise
        # `ValueError: Not valid is not valid` out of InputFile.__new__.
        file = InputFile(self.fullpath)
        self.assertIsInstance(file, InputFileTemplate)
        self.assertEqual(file.product, "not valid")
        self.assertEqual(len(file.variables), 0)


class TestInputFileDispatch(unittest.TestCase):
    """InputFile.__new__ detects the product, dispatches to the class for it, and
    does both while reading each of the input file and the config exactly once.
    """

    def _counting_open(self, counter):
        real_open = builtins.open

        def counted(*args, **kwargs):
            counter.append(args[0] if args else kwargs.get("file"))
            return real_open(*args, **kwargs)

        return counted

    def test_reads_the_input_file_once(self):
        fullpath = folder_nnp / "only_variables.in"
        opened = []
        with unittest.mock.patch.object(builtins, "open", self._counting_open(opened)):
            InputFile(fullpath)
        reads = [p for p in opened if Path(p) == fullpath]
        # __new__ reads the text to detect the product and hands it to the class it
        # picks, so the load does not go back to disk for the same bytes.
        self.assertEqual(len(reads), 1)

    def test_builds_the_config_once(self):
        fullpath = folder_nnp / "only_variables.in"
        real_init = defaults.NNConfig.__init__
        calls = []

        def counted(self, *args, **kwargs):
            calls.append(1)
            return real_init(self, *args, **kwargs)

        with unittest.mock.patch.object(defaults.NNConfig, "__init__", counted):
            InputFile(fullpath)
        # only the returned object builds a config; product detection needs none.
        self.assertEqual(len(calls), 1)

    def test_dispatches_on_product(self):
        # every product must reach its own InputFile class.
        cases = [
            (folder_nnp / "only_variables.in", "nextnano++"),
            (folder_nnp / "example.in", "nextnano++"),
            (folder_nn3 / "only_variables.in", "nextnano3"),
            (folder_nn3 / "example.in", "nextnano3"),
            (
                Path("tests") / "datafiles" / "nextnano.NEGF" / "example.xml",
                "nextnano.NEGF_classic",
            ),
            (Path("tests") / "datafiles" / "nextnano.MSB" / "example.msb", "nextnano.MSB"),
        ]
        for fullpath, product in cases:
            with self.subTest(fullpath=fullpath):
                file = InputFile(fullpath)
                self.assertEqual(file.product, product)
                self.assertIsInstance(file, defaults.get_InputFile(product))

    def test_no_fullpath_gives_a_bare_template(self):
        # with no path there is no text to detect from: InputFile() is an empty
        # InputFileTemplate carrying the 'not valid' sentinel. __new__ must not open None.
        file = InputFile()
        self.assertIsInstance(file, InputFileTemplate)
        self.assertEqual(file.product, "not valid")
        self.assertIsNone(file.fullpath)


class TestSweep(unittest.TestCase):
    def test_init(self):
        self.assertRaises(TypeError, Sweep)
        sweep = Sweep({})
        self.assertEqual(sweep.fullpath, None)
        self.assertEqual(sweep.var_sweep, {})
        self.assertRaises(ValueError, Sweep, {"Name": "some_name"})

    def test_nnp_init(self):
        fullpath = folder_nnp / "only_variables.in"
        self.assertRaises(ValueError, Sweep, {"Name": "some_name"}, fullpath)

        sweep = Sweep({}, fullpath)
        self.assertEqual(Path(sweep.fullpath), fullpath)
        self.assertEqual(sweep.var_sweep, {})
        self.assertFalse(sweep.input_files)
        self.assertFalse(sweep.sweep_output_directory)

        self.assertRaises(ValueError, Sweep, {"float": 1})
        self.assertRaises(TypeError, Sweep, {"float": 1}, fullpath)

        sweep = Sweep({"float": [1, 2, 5]}, fullpath)
        self.assertEqual(Path(sweep.fullpath), fullpath)
        self.assertEqual(sweep.var_sweep["float"], [1, 2, 5])

        self.addCleanup(
            delete_files,
            "only_variables",
            directory=folder_nnp,
            exceptions=["only_variables.in"],
        )

    def test_nnp_mkdir(self):
        fullpath = folder_nnp / "only_variables.in"
        sweep = Sweep({}, fullpath=fullpath)
        sweep.config.set("nextnano++", "outputdirectory", r"tests//outputs")
        created_directory = sweep.mk_dir(overwrite=True)
        self.assertTrue(
            Path(created_directory).samefile(Path("tests") / "outputs" / "only_variables_sweep")
        )
        self.assertTrue((Path("tests") / "outputs" / "only_variables_sweep").is_dir())

        self.addCleanup((Path("tests") / "outputs" / "only_variables_sweep").rmdir)
        self.addCleanup(
            delete_files,
            "only_variables",
            directory=folder_nnp,
            exceptions=["only_variables.in"],
        )

    def test_nnp_mkdir_specify(self):
        fullpath = folder_nnp / "only_variables.in"
        sweep = Sweep({}, fullpath=fullpath)
        created_directory = sweep.mk_dir(overwrite=True, output_directory=r"tests//outputs")
        self.assertTrue(
            Path(created_directory).samefile(Path("tests") / "outputs" / "only_variables_sweep")
        )
        self.assertTrue((Path("tests") / "outputs" / "only_variables_sweep").is_dir())

        self.addCleanup((Path("tests") / "outputs" / "only_variables_sweep").rmdir)
        self.addCleanup(
            delete_files,
            "only_variables",
            directory=folder_nnp,
            exceptions=["only_variables.in"],
        )

    def test_nnp_save(self):
        self.addCleanup(
            delete_files,
            "only_variables",
            directory=folder_nnp,
            exceptions=["only_variables.in"],
        )
        fullpath = folder_nnp / "only_variables.in"
        sweep = Sweep({"float": [1, 2], "str": ["test1", "test2"]}, fullpath)
        sweep.save_sweep()

        files_with_names = [p.name for p in folder_nnp.iterdir() if "only_variables" in p.name]
        self.assertEqual(len(files_with_names), 5)
        self.assertTrue((folder_nnp / "only_variables__float_2_str_test1_.in").is_file())

    def test_nnp_save_temp(self):
        self.addCleanup(
            delete_files,
            "only_variables",
            directory=folder_nnp,
            exceptions=["only_variables.in"],
        )

        fullpath = folder_nnp / "only_variables.in"
        sweep = Sweep({"float": [1, 2], "str": ["test1", "test2"]}, fullpath)
        sweep.save_sweep(temp=True)

        files_with_names = [file for file in os.listdir(folder_nnp) if "only_variables" in file]
        self.assertEqual(len(files_with_names), 1)
        self.assertFalse((folder_nnp / "only_variables__float_2_str_test1_.in").is_file())

    # nn3 section
    def test_nn3_init(self):
        fullpath = folder_nn3 / "only_variables.in"
        self.assertRaises(ValueError, Sweep, {"Name": "some_name"}, fullpath)

        sweep = Sweep({}, fullpath)
        self.assertEqual(Path(sweep.fullpath), fullpath)
        self.assertEqual(sweep.var_sweep, {})
        self.assertFalse(sweep.input_files)
        self.assertFalse(sweep.sweep_output_directory)

        self.assertRaises(ValueError, Sweep, {"float": 1})
        self.assertRaises(TypeError, Sweep, {"float": 1}, fullpath)

        sweep = Sweep({"float": [1, 2, 5]}, fullpath)
        self.assertEqual(Path(sweep.fullpath), fullpath)
        self.assertEqual(sweep.var_sweep["float"], [1, 2, 5])

        self.addCleanup(
            delete_files,
            "only_variables",
            directory=folder_nn3,
            exceptions=["only_variables.in"],
        )

    def test_nn3_mkdir(self):
        fullpath = folder_nn3 / "only_variables.in"
        sweep = Sweep({}, fullpath=fullpath)
        sweep.config.set("nextnano3", "outputdirectory", r"tests//outputs")
        created_directory = sweep.mk_dir(overwrite=True)
        self.assertTrue(
            Path(created_directory).samefile(Path("tests") / "outputs" / "only_variables_sweep")
        )
        self.assertTrue((Path("tests") / "outputs" / "only_variables_sweep").is_dir())

        self.addCleanup((Path("tests") / "outputs" / "only_variables_sweep").rmdir)
        self.addCleanup(
            delete_files,
            "only_variables",
            directory=folder_nn3,
            exceptions=["only_variables.in"],
        )

    def test_nn3_save(self):
        self.addCleanup(
            delete_files,
            "only_variables",
            directory=folder_nn3,
            exceptions=["only_variables.in"],
        )
        fullpath = folder_nn3 / "only_variables.in"
        sweep = Sweep({"float": [1, 2], "str": ["test1", "test2"]}, fullpath)
        sweep.save_sweep()

        files_with_names = [p.name for p in folder_nn3.iterdir() if "only_variables" in p.name]
        self.assertEqual(len(files_with_names), 5)
        self.assertTrue((folder_nn3 / "only_variables__float_2_str_test1_.in").is_file())

    # TODO test parallel sweeps with and without convergenceCheck
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        sweep_dir = Path("tests") / "outputs" / "only_variables_sweep"
        if sweep_dir.is_dir():
            sweep_dir.rmdir()
        delete_files("only_variables", directory=folder_nnp, exceptions=["only_variables.in"])
        delete_files("only_variables", directory=folder_nn3, exceptions=["only_variables.in"])

    def test_conditional_sweep(self):
        self.addCleanup(
            delete_files,
            "only_variables",
            directory=folder_nnp,
            exceptions=["only_variables.in"],
        )

        def condition(combination):
            return combination[0] > 0.2

        fullpath = folder_nnp / "only_variables.in"
        sweep = Sweep(
            {"float": [0.1, 0.2, 0.3, 0.4, 0.5]},
            fullpath,
        )

        sweep.save_sweep(variables_comb_screen_fn=condition)

        self.assertEqual(len(sweep.input_files), 3)

        for combination in sweep.sweep_infodict.values():
            combination = list(combination.values())
            assert combination[0] > 0.2

    def test_conditional_sweep_multivar(self):
        self.addCleanup(
            delete_files,
            "only_variables",
            directory=folder_nnp,
            exceptions=["only_variables.in"],
        )

        def condition(combination):
            return combination[1] > combination[0]

        fullpath = folder_nnp / "only_variables.in"
        sweep = Sweep(
            {"float": [0.5, 1.5, 2.5], "int": [1, 2, 3]},
            fullpath,
        )
        sweep.save_sweep(variables_comb_screen_fn=condition)

        self.assertEqual(len(sweep.input_files), 6)

        for combination in sweep.sweep_infodict.values():
            combination = list(combination.values())
            self.assertTrue(combination[1] > combination[0])


class Test_check_convergence_pause_tty(unittest.TestCase):
    """check_convergence(mode='pause') must never block on input() without a TTY.

    Headless runs (CI, cluster jobs, the ExecutionQueue worker thread) have no
    usable stdin; 'pause' must degrade to 'terminate' there instead of hanging.
    """

    NOT_CONVERGED = "Maximum number of iterations exceeded\n"

    def make_file(self, log_text):
        tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(tmpdir.cleanup)
        log = Path(tmpdir.name) / "sim.log"
        log.write_text(log_text)
        file = InputFile(folder_nnp / "only_variables.in")
        file.execute_info = {"logfile": str(log)}
        return file

    def test_pause_without_tty_terminates_instead_of_prompting(self):
        file = self.make_file(self.NOT_CONVERGED)
        stdin = unittest.mock.Mock()
        stdin.isatty.return_value = False
        prompt = unittest.mock.Mock(side_effect=AssertionError("input() called without a TTY"))
        with (
            unittest.mock.patch("sys.stdin", stdin),
            unittest.mock.patch("builtins.input", prompt),
        ):
            with self.assertRaises(RuntimeError):
                file.check_convergence(mode="pause")
        prompt.assert_not_called()

    def test_pause_with_stdin_none_terminates(self):
        # sys.stdin is None under pythonw / some embedded interpreters
        file = self.make_file(self.NOT_CONVERGED)
        with unittest.mock.patch("sys.stdin", None):
            with self.assertRaises(RuntimeError):
                file.check_convergence(mode="pause")

    def test_pause_with_tty_still_prompts(self):
        file = self.make_file(self.NOT_CONVERGED)
        stdin = unittest.mock.Mock()
        stdin.isatty.return_value = True
        with (
            unittest.mock.patch("sys.stdin", stdin),
            unittest.mock.patch("builtins.input", return_value="y") as prompt,
        ):
            self.assertIsNone(file.check_convergence(mode="pause"))
        prompt.assert_called()

        with (
            unittest.mock.patch("sys.stdin", stdin),
            unittest.mock.patch("builtins.input", return_value="n"),
        ):
            with self.assertRaises(RuntimeError):
                file.check_convergence(mode="pause")

    def test_converged_log_never_prompts(self):
        file = self.make_file("everything fine\n")
        prompt = unittest.mock.Mock(side_effect=AssertionError("input() called for converged log"))
        with unittest.mock.patch("builtins.input", prompt):
            self.assertIsNone(file.check_convergence(mode="pause"))


if __name__ == "__main__":
    unittest.main()

    file = folder_nnp / "only_variables.in"
    fi = InputFile(file)
    text = fi.text
