import unittest
import os

from .txt_storage import TxtStorage


class TestTxtStorage(unittest.TestCase):
    def setUp(self):
        self.storage = TxtStorage()
        self.test_data = {'key1': 'value1', 'key2': [{'key1': 'item1'}, 'item2'], 'key3': {'subkey1': 1, 'subkey2': 2}}
        self.filename = 'test_data.txt'

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_save_load(self):
        self.storage.save(self.test_data, self.filename)
        self.assertTrue(os.path.exists(self.filename))
        loaded_data = self.storage.load(self.filename)
        self.assertEqual(loaded_data, self.test_data)


if __name__ == '__main__':
    unittest.main()
