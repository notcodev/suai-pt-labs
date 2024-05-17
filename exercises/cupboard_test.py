import unittest
from unittest.mock import MagicMock, patch, mock_open
from .cupboard import Cupboard, InsufficientItemQuantityError
from storages.interface import StorageInterface
from storages.txt_storage import TxtStorage

from storages.interface import StorageInterface

class TestStorage(StorageInterface):
    def __init__(self):
        self.data = {}

    def save(self, data, filename):
        self.data[filename] = data

    def load(self, filename):
        return self.data.get(filename, {})


class TestCupboard(unittest.TestCase):
    def setUp(self):
        self.cupboard = Cupboard()

    def test_save_load_state(self):
        storage = MagicMock(spec=StorageInterface)
        filename = "test_portfolio_state.mock"
        expected_data = {'item1': 10, 'item2': 5}

        self.cupboard.add_item("item1", 10)
        self.cupboard.add_item("item2", 5)

        self.cupboard.save_state(storage, filename)
        storage.save.assert_called_once_with(expected_data, filename)

        new_cupboard = Cupboard()
        storage.load.return_value = expected_data

        new_cupboard.load_state(storage, filename)
        storage.load.assert_called_once_with(filename)

        self.assertEqual(new_cupboard.items, self.cupboard.items)

    def test_add_item(self):
        self.cupboard.add_item("item1", 10)
        self.assertEqual(self.cupboard.items["item1"], 10)

        self.cupboard.add_item("item1", 5)
        self.assertEqual(self.cupboard.items["item1"], 15)

    def test_remove_item(self):
        self.cupboard.add_item("item1", 10)
        self.cupboard.remove_item("item1", 5)
        self.assertEqual(self.cupboard.items["item1"], 5)

        self.cupboard.remove_item("item1", 5)
        self.assertNotIn("item1", self.cupboard.items)

    def test_remove_item_insufficient_quantity(self):
        self.cupboard.add_item("item1", 5)
        with self.assertRaises(InsufficientItemQuantityError):
            self.cupboard.remove_item("item1", 10)

    def test_remove_item_not_exists(self):
        with self.assertRaises(InsufficientItemQuantityError):
            self.cupboard.remove_item("item1", 1)


if __name__ == '__main__':
    unittest.main()
