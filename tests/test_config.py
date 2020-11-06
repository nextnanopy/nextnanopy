import os
from nextnanopy.utils.config import Config, NNConfig
import unittest


class Test_NNConfig(unittest.TestCase):
    def test_default(self):
        config = NNConfig()
        default_fullpath = os.path.join(os.environ['HOMEDRIVE'], os.environ['HOMEPATH'], '.nnconfig')

        self.assertEqual(config.fullpath, default_fullpath)
        self.assertTrue('nextnano3' in config.validators.keys())
        self.assertTrue('nextnano++' in config.validators.keys())
        self.assertTrue('nextnano3' in config.default.keys())
        self.assertTrue('nextnano++' in config.default.keys())
        self.assertTrue('nextnano3' in config.config.keys())
        self.assertTrue('nextnano++' in config.config.keys())
        compulsory_options = ['exe', 'license', 'database', 'threads', 'outputdirectory']
        for option in compulsory_options:
            self.assertTrue(option in config.validators['nextnano3'].keys())
            self.assertTrue(option in config.validators['nextnano++'].keys())
            self.assertTrue(option in config.default['nextnano3'].keys())
            self.assertTrue(option in config.default['nextnano++'].keys())
            self.assertTrue(option in config.config['nextnano3'].keys())
            self.assertTrue(option in config.config['nextnano++'].keys())
        self.assertTrue(os.path.isfile(config.fullpath))
        if os.path.isfile(config.fullpath):
            os.remove(config.fullpath)

    def test_load(self):
        fullpath = os.path.join('tests', '.nnconfig')
        config = NNConfig(fullpath)

        self.assertEqual(config.fullpath, fullpath)
        self.assertTrue('nextnano3' in config.validators.keys())
        self.assertTrue('nextnano++' in config.validators.keys())
        self.assertTrue('nextnano3' in config.default.keys())
        self.assertTrue('nextnano++' in config.default.keys())
        self.assertTrue('nextnano3' in config.config.keys())
        self.assertTrue('nextnano++' in config.config.keys())
        compulsory_options = ['exe', 'license', 'database', 'threads', 'outputdirectory']
        for option in compulsory_options:
            self.assertTrue(option in config.validators['nextnano3'].keys())
            self.assertTrue(option in config.validators['nextnano++'].keys())
            self.assertTrue(option in config.default['nextnano3'].keys())
            self.assertTrue(option in config.default['nextnano++'].keys())
            self.assertTrue(option in config.config['nextnano3'].keys())
            self.assertTrue(option in config.config['nextnano++'].keys())
        self.assertTrue(os.path.isfile(config.fullpath))

        self.assertEqual(config.config['nextnano++']['exe'], '')
        config.set('nextnano++', 'exe', 'some_path')
        self.assertEqual(config.config['nextnano++']['exe'], 'some_path')
        config.to_default()
        self.assertEqual(config.config['nextnano++']['exe'], '')
        if os.path.isfile(config.fullpath):
            os.remove(config.fullpath)
        fullpath_new = os.path.join('tests', 'test.nnconfig')
        self.assertFalse(os.path.isfile(fullpath_new))
        config.save(fullpath_new)
        self.assertTrue(os.path.isfile(fullpath_new))
        self.assertEqual(config.fullpath, fullpath_new)
        if os.path.isfile(config.fullpath):
            os.remove(config.fullpath)

if __name__ == '__main__':
    unittest.main()
