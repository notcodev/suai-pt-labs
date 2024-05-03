import json
import unittest
import os

from .json_storage import JsonStorage


class TestJsonStorage(unittest.TestCase):
    def setUp(self):
        self.storage = JsonStorage()
        self.test_data = {'key1': 'value1', 'key2': 'value2'}
        self.filename = 'test_data.json'

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_save(self):
        self.storage.save(self.test_data, self.filename)
        self.assertTrue(os.path.exists(self.filename))
        with open(self.filename, 'r') as file:
            saved_data = json.load(file)
            self.assertEqual(saved_data, self.test_data)

    def test_load(self):
        with open(self.filename, 'w') as file:
            json.dump(self.test_data, file)
        loaded_data = self.storage.load(self.filename)
        self.assertEqual(loaded_data, self.test_data)


if __name__ == '__main__':
    unittest.main()
