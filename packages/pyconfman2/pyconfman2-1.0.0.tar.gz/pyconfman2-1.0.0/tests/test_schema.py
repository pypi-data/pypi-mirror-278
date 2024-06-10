import unittest
import os
import yaml
from src.pyconfman2.Schema import ConfigSchema
from src.pyconfman2.Exceptions import InvalidPropertyError, EmptyValueProperty, KeyExistsError

class TestConfigSchema(unittest.TestCase):

    def setUp(self):
        self.default_schema = {'key1': 'value1', 'key2': 'value2'}
        self.config_schema = ConfigSchema(default_schema=self.default_schema)
    
    def tearDown(self):
        for file in ['test_config.yaml', 'config.yaml', 'config.yml']:
            if os.path.exists(file):
                os.remove(file)
                
    def test_init_with_invalid_schema(self):
        with self.assertRaises(InvalidPropertyError):
            ConfigSchema(default_schema=[])

    def test_str(self):
        self.assertEqual(str(self.config_schema), str(self.default_schema))

    def test_add_with_dict(self):
        new_props = {'key2': 'new_value2', 'key3': 'value3'}
        self.config_schema.add(new_props)
        self.assertEqual(self.config_schema.properties['key2'], 'new_value2')
        self.assertEqual(self.config_schema.properties['key3'], 'value3')

    def test_add_with_key_value(self):
        self.config_schema.add('key3', 'value3')
        self.assertEqual(self.config_schema.properties['key3'], 'value3')

    def test_add_without_value(self):
        with self.assertRaises(EmptyValueProperty):
            self.config_schema.add('key3', None)

    def test_add_without_override(self):
        # Key 'key2' should retain its original value because override is set to False
        self.config_schema.add('key2', 'another_value2', override=False)
        self.assertEqual(self.config_schema.properties['key2'], 'value2')

    def test_get(self):
        self.assertEqual(self.config_schema.get('key1'), 'value1')
    
    def test_get_strict(self):
        with self.assertRaises(KeyError):
            self.config_schema.get('nonexistent_key', strict=True)
    
    def test_remove(self):
        self.config_schema.remove('key1')
        self.assertNotIn('key1', self.config_schema.properties)

    def test_remove_strict(self):
        with self.assertRaises(KeyError):
            self.config_schema.remove('nonexistent_key', strict=True)

    def test_load(self):
        test_config = {'key3': 'value3', 'key4': 'value4'}
        with open('test_config.yaml', 'w') as file:
            yaml.safe_dump(test_config, file)

        self.config_schema.load('test_config.yaml')
        self.assertEqual(self.config_schema.properties['key3'], 'value3')
        self.assertEqual(self.config_schema.properties['key4'], 'value4')

    def test_load_nonexistent_file(self):
        with self.assertRaises(FileNotFoundError):
            self.config_schema.load('nonexistent_file.yaml')

    def test_items(self):
        self.assertEqual(list(self.config_schema.items()), list(self.default_schema.items()))

    def test_iteration(self):
        keys = [key for key in self.config_schema]
        self.assertEqual(keys, list(self.default_schema.items()))

    def test_search_for_default_config_file(self):
        default_config = {'key4': 'value4', 'key5': 'value5'}
        with open('config.yaml', 'w') as file:
            yaml.safe_dump(default_config, file)

        new_config_schema = ConfigSchema()
        self.assertEqual(new_config_schema.properties['key4'], 'value4')
        self.assertEqual(new_config_schema.properties['key5'], 'value5')

if __name__ == '__main__':
    unittest.main()