import unittest
from unittest.mock import mock_open, patch
from .txt_storage import TxtStorage

class TestTxtStorage(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open)
    def test_save(self, mock_file):
        storage = TxtStorage()
        data = {
            'item1': 'description1',
            'item2': 42,
            'item3': True,
            'item4': 3.14,
            'item5': ['a', 'b', 'c'],
            'item6': {'subitem1': 'subdescription1', 'subitem2': 99}
        }

        storage.save(data, 'mockfile.txt')

        mock_file.assert_called_once_with('mockfile.txt', 'w')
        mock_file_handle = mock_file()

        expected_calls = [
            'str|item1|str:description1\n',
            'str|item2|int:42\n',
            'str|item3|bool:True\n',
            'str|item4|float:3.14\n',
            'str|item5|list:int|0|str:a\n',
            'str|item5|list:int|1|str:b\n',
            'str|item5|list:int|2|str:c\n',
            'str|item6|dict:str|subitem1|str:subdescription1\n',
            'str|item6|dict:str|subitem2|int:99\n'
        ]

        actual_calls = [call.args[0] for call in mock_file_handle.write.mock_calls]
        self.assertEqual(expected_calls, actual_calls)

    @patch('builtins.open', new_callable=mock_open, read_data=(
        'str|item1|str:description1\n'
        'str|item2|int:42\n'
        'str|item3|bool:True\n'
        'str|item4|float:3.14\n'
        'str|item5|list:int|0|str:a\n'
        'str|item5|list:int|1|str:b\n'
        'str|item5|list:int|2|str:c\n'
        'str|item6|dict:str|subitem1|str:subdescription1\n'
        'str|item6|dict:str|subitem2|int:99\n'
    ))
    def test_load(self, mock_file):
        storage = TxtStorage()
        expected_data = {
            'item1': 'description1',
            'item2': 42,
            'item3': True,
            'item4': 3.14,
            'item5': ['a', 'b', 'c'],
            'item6': {'subitem1': 'subdescription1', 'subitem2': 99}
        }

        data = storage.load('mockfile.txt')

        mock_file.assert_called_once_with('mockfile.txt', 'r')
        self.assertEqual(data, expected_data)

if __name__ == '__main__':
    unittest.main()
