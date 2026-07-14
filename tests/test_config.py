import tempfile
import unittest
import warnings
from pathlib import Path
from unittest import mock

from nextnanopy.defaults import NNConfig
from nextnanopy.utils.config import Config

default_config_path = Path.home() / ".nextnanopy-config"


class Test_NNConfig(unittest.TestCase):
    def test_default_nn3(self):
        config = NNConfig()

        self.assertEqual(Path(config.fullpath), default_config_path)
        self.assertTrue("nextnano3" in config.validators.keys())
        self.assertTrue("nextnano3" in config.defaults.keys())
        self.assertTrue("nextnano3" in config.config.keys())
        options = [
            "exe",
            "license",
            "database",
            "threads",
            "outputdirectory",
            "debuglevel",
            "cancel",
            "softkill",
        ]
        for option in options:
            self.assertTrue(option in config.validators["nextnano3"].keys())
            self.assertTrue(option in config.defaults["nextnano3"].keys())
            self.assertTrue(option in config.config["nextnano3"].keys())
        self.assertTrue(Path(config.fullpath).is_file())

    def test_default_nnp(self):
        config = NNConfig()
        self.assertEqual(Path(config.fullpath), default_config_path)
        self.assertTrue("nextnano++" in config.validators.keys())
        self.assertTrue("nextnano++" in config.defaults.keys())
        self.assertTrue("nextnano++" in config.config.keys())
        options = ["exe", "license", "database", "threads", "outputdirectory"]
        for option in options:
            self.assertTrue(option in config.validators["nextnano++"].keys())
            self.assertTrue(option in config.defaults["nextnano++"].keys())
            self.assertTrue(option in config.config["nextnano++"].keys())
        self.assertTrue(Path(config.fullpath).is_file())

    def test_default_negf(self):
        config = NNConfig()
        self.assertEqual(Path(config.fullpath), default_config_path)
        self.assertTrue("nextnano.NEGF" in config.validators.keys())
        self.assertTrue("nextnano.NEGF" in config.defaults.keys())
        self.assertTrue("nextnano.NEGF" in config.config.keys())
        options = ["exe", "license", "database", "threads", "outputdirectory"]
        for option in options:
            self.assertTrue(option in config.validators["nextnano.NEGF"].keys())
            self.assertTrue(option in config.defaults["nextnano.NEGF"].keys())
            self.assertTrue(option in config.config["nextnano.NEGF"].keys())
        self.assertTrue(Path(config.fullpath).is_file())

    def test_default_nnevo(self):
        config = NNConfig()
        self.assertEqual(Path(config.fullpath), default_config_path)
        self.assertTrue("nextnanoevo" in config.validators.keys())
        self.assertTrue("nextnanoevo" in config.defaults.keys())
        self.assertTrue("nextnanoevo" in config.config.keys())
        options = ["license"]
        for option in options:
            self.assertTrue(option in config.validators["nextnanoevo"].keys())
            self.assertTrue(option in config.defaults["nextnanoevo"].keys())
            self.assertTrue(option in config.config["nextnanoevo"].keys())
        option = "exe"  # no exe for nnevo
        self.assertFalse(option in config.validators["nextnanoevo"].keys())
        self.assertFalse(option in config.defaults["nextnanoevo"].keys())
        self.assertFalse(option in config.config["nextnanoevo"].keys())
        self.assertTrue(Path(config.fullpath).is_file())

    def test_load_nn3(self):
        fullpath = Path("tests") / ".nextnanopy-config"
        config = NNConfig(fullpath)

        self.assertEqual(Path(config.fullpath), fullpath)
        self.assertTrue("nextnano3" in config.validators.keys())
        self.assertTrue("nextnano3" in config.defaults.keys())
        self.assertTrue("nextnano3" in config.config.keys())
        options = [
            "exe",
            "license",
            "database",
            "threads",
            "outputdirectory",
            "debuglevel",
            "cancel",
            "softkill",
        ]
        for option in options:
            self.assertTrue(option in config.validators["nextnano3"].keys())
            self.assertTrue(option in config.defaults["nextnano3"].keys())
            self.assertTrue(option in config.config["nextnano3"].keys())
        self.assertTrue(Path(config.fullpath).is_file())
        if Path(config.fullpath).is_file():
            Path(config.fullpath).unlink()

        self.assertEqual(config.config["nextnano3"]["exe"], "")
        config.set("nextnano3", "exe", "some_path")
        self.assertEqual(config.config["nextnano3"]["exe"], "some_path")
        config.to_default()
        self.assertEqual(config.config["nextnano3"]["exe"], "")
        if Path(config.fullpath).is_file():
            Path(config.fullpath).unlink()
        fullpath_new = Path("tests") / "test.nnconfig"
        self.assertFalse(fullpath_new.is_file())
        config.save(fullpath_new)
        self.assertTrue(fullpath_new.is_file())
        self.assertEqual(Path(config.fullpath), fullpath_new)
        if Path(config.fullpath).is_file():
            Path(config.fullpath).unlink()

    def test_load_nnp(self):
        fullpath = Path("tests") / ".nextnanopy-config"
        config = NNConfig(fullpath)

        self.assertEqual(Path(config.fullpath), fullpath)
        self.assertTrue("nextnano++" in config.validators.keys())
        self.assertTrue("nextnano++" in config.defaults.keys())
        self.assertTrue("nextnano++" in config.config.keys())
        options = ["exe", "license", "database", "threads", "outputdirectory"]
        for option in options:
            self.assertTrue(option in config.validators["nextnano++"].keys())
            self.assertTrue(option in config.defaults["nextnano++"].keys())
            self.assertTrue(option in config.config["nextnano++"].keys())
        self.assertTrue(Path(config.fullpath).is_file())
        if Path(config.fullpath).is_file():
            Path(config.fullpath).unlink()

        self.assertEqual(config.config["nextnano++"]["exe"], "")
        config.set("nextnano++", "exe", "some_path")
        self.assertEqual(config.config["nextnano++"]["exe"], "some_path")
        config.to_default()
        self.assertEqual(config.config["nextnano++"]["exe"], "")
        if Path(config.fullpath).is_file():
            Path(config.fullpath).unlink()
        fullpath_new = Path("tests") / "test.nnconfig"
        self.assertFalse(fullpath_new.is_file())
        config.save(fullpath_new)
        self.assertTrue(fullpath_new.is_file())
        self.assertEqual(Path(config.fullpath), fullpath_new)
        if Path(config.fullpath).is_file():
            Path(config.fullpath).unlink()

    def test_load_negf(self):
        fullpath = Path("tests") / ".nextnanopy-config"
        config = NNConfig(fullpath)

        self.assertEqual(Path(config.fullpath), fullpath)
        self.assertTrue("nextnano.NEGF" in config.validators.keys())
        self.assertTrue("nextnano.NEGF" in config.defaults.keys())
        self.assertTrue("nextnano.NEGF" in config.config.keys())
        options = ["exe", "license", "database", "threads", "outputdirectory"]
        for option in options:
            self.assertTrue(option in config.validators["nextnano.NEGF"].keys())
            self.assertTrue(option in config.defaults["nextnano.NEGF"].keys())
            self.assertTrue(option in config.config["nextnano.NEGF"].keys())
        self.assertTrue(Path(config.fullpath).is_file())
        if Path(config.fullpath).is_file():
            Path(config.fullpath).unlink()

        self.assertEqual(config.config["nextnano.NEGF"]["exe"], "")
        config.set("nextnano.NEGF", "exe", "some_path")
        self.assertEqual(config.config["nextnano.NEGF"]["exe"], "some_path")
        config.to_default()
        self.assertEqual(config.config["nextnano.NEGF"]["exe"], "")
        if Path(config.fullpath).is_file():
            Path(config.fullpath).unlink()
        fullpath_new = Path("tests") / "test.nnconfig"
        self.assertFalse(fullpath_new.is_file())
        config.save(fullpath_new)
        self.assertTrue(fullpath_new.is_file())
        self.assertEqual(Path(config.fullpath), fullpath_new)
        if Path(config.fullpath).is_file():
            Path(config.fullpath).unlink()

    def test_get_unsupported_products(self):
        filepath = Path("tests") / "configs" / ".nnconfig_unsupported"
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            config = NNConfig(filepath)
        unsupported_products = set(config.get_unsupported_products())
        self.assertEqual(
            unsupported_products,
            {"nextnano.NEGF++", "nextnano_nonexistent"},
        )


class Test_Config(unittest.TestCase):
    def test_falsy_fullpath_raises(self):
        for fullpath in ["", None]:
            with self.assertRaises(ValueError):
                Config(fullpath)

    def test_missing_file_yields_empty_config(self):
        with tempfile.TemporaryDirectory() as folder:
            fullpath = Path(folder) / "missing.nnconfig"
            config = Config(str(fullpath))

            self.assertEqual(list(config.sections), [])
            self.assertEqual(Path(config.fullpath), fullpath)

    def test_save_creates_missing_file(self):
        with tempfile.TemporaryDirectory() as folder:
            fullpath = Path(folder) / "new.nnconfig"
            config = Config(str(fullpath))
            config.add_section("nextnano++")
            config.set("nextnano++", "exe", "some_path")
            config.save()

            self.assertTrue(fullpath.is_file())
            self.assertEqual(Config(str(fullpath)).get("nextnano++", "exe"), "some_path")

    def test_set_without_save_does_not_create_file(self):
        with tempfile.TemporaryDirectory() as folder:
            fullpath = Path(folder) / "unsaved.nnconfig"
            config = Config(str(fullpath))
            config.add_section("nextnano++")
            config.set("nextnano++", "exe", "some_path")

            self.assertEqual(config.get("nextnano++", "exe"), "some_path")
            self.assertFalse(fullpath.is_file())

    def test_set_without_save_does_not_change_file(self):
        with tempfile.TemporaryDirectory() as folder:
            fullpath = Path(folder) / "existing.nnconfig"
            config = Config(str(fullpath))
            config.add_section("nextnano++")
            config.set("nextnano++", "exe", "original")
            config.save()

            config.set("nextnano++", "exe", "modified")

            self.assertEqual(config.get("nextnano++", "exe"), "modified")
            self.assertEqual(Config(str(fullpath)).get("nextnano++", "exe"), "original")

    def test_empty_fullpath_raises_for_nnconfig(self):
        # None means 'use the default path', but an empty path is a caller bug
        # and must not be silently treated as the default.
        with self.assertRaises(ValueError):
            NNConfig("")

    def test_save_to_new_path_leaves_no_temp_file(self):
        with tempfile.TemporaryDirectory() as folder:
            fullpath = Path(folder) / "first.nnconfig"
            config = Config(str(fullpath))
            config.add_section("nextnano++")
            config.set("nextnano++", "exe", "some_path")
            config.save()

            new_fullpath = Path(folder) / "second.nnconfig"
            config.save(str(new_fullpath))

            self.assertEqual(Path(config.fullpath), new_fullpath)
            self.assertEqual(Config(str(new_fullpath)).get("nextnano++", "exe"), "some_path")
            self.assertEqual(
                sorted(p.name for p in Path(folder).iterdir()),
                ["first.nnconfig", "second.nnconfig"],
            )

    def test_failed_save_keeps_previous_file_and_leaves_no_temp_file(self):
        # save() writes a temp file and swaps it in with os.replace, so a write that
        # blows up half way must not truncate the config that is already on disk.
        with tempfile.TemporaryDirectory() as folder:
            fullpath = Path(folder) / "existing.nnconfig"
            config = Config(str(fullpath))
            config.add_section("nextnano++")
            config.set("nextnano++", "exe", "original")
            config.save()

            config.set("nextnano++", "exe", "modified")
            with mock.patch.object(
                config.configparser, "write", side_effect=OSError("disk full")
            ):
                with self.assertRaises(OSError):
                    config.save()

            self.assertEqual(Config(str(fullpath)).get("nextnano++", "exe"), "original")
            self.assertEqual([p.name for p in Path(folder).iterdir()], ["existing.nnconfig"])


if __name__ == "__main__":
    unittest.main()
