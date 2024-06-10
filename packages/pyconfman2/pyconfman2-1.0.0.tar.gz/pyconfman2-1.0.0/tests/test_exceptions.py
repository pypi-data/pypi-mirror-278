import unittest
from src.pyconfman2.Exceptions import InvalidPropertyError, EmptyValueProperty, KeyExistsError

class TestExceptions(unittest.TestCase):

    def test_invalid_property_error(self):
        with self.assertRaises(InvalidPropertyError) as context:
            raise InvalidPropertyError("Custom message.")
        self.assertEqual(str(context.exception), "Custom message.")

    def test_empty_value_property(self):
        with self.assertRaises(EmptyValueProperty) as context:
            raise EmptyValueProperty("Custom message.")
        self.assertEqual(str(context.exception), "Custom message.")
    
    def test_key_exists_error(self):
        with self.assertRaises(KeyExistsError) as context:
            raise KeyExistsError("Custom message.")
        self.assertEqual(str(context.exception), "Custom message.")

if __name__ == '__main__':
    unittest.main()