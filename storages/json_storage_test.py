import unittest
from unittest.mock import mock_open, patch

from .json_storage import JsonStorage

class TestJSONStorage(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save(self, mock_json_dump, mock_file):
        storage = JsonStorage()
        data = {'item1': 'description1', 'item2': 'description2'}

        storage.save(data, 'mockfile.json')

        mock_file.assert_called_once_with('mockfile.json', 'w')
        mock_json_dump.assert_called_once_with(data, mock_file(), indent=4)

    @patch('builtins.open', new_callable=mock_open, read_data='{"item1": "description1", "item2": "description2"}')
    @patch('json.load')
    def test_load(self, mock_json_load, mock_file):
        storage = JsonStorage()
        expected_data = {'item1': 'description1', 'item2': 'description2'}
        mock_json_load.return_value = expected_data

        data = storage.load('mockfile.json')

        mock_file.assert_called_once_with('mockfile.json', 'r')
        mock_json_load.assert_called_once_with(mock_file())
        self.assertEqual(data, expected_data)

if __name__ == '__main__':
    unittest.main()
