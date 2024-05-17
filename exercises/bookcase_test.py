import unittest
from unittest.mock import MagicMock, mock_open, patch

from storages.interface import StorageInterface
from .bookcase import Book, Bookcase, MaxWeightExceededError, BookNotFoundError
from storages.txt_storage import TxtStorage

class TestStorage(StorageInterface):
    def __init__(self):
        self.data = {}

    def save(self, data, filename):
        self.data[filename] = data

    def load(self, filename):
        return self.data.get(filename, {})


class TestBookcase(unittest.TestCase):
    def setUp(self):
        self.bookcase = Bookcase(max_weight=100)
        self.books = [
            Book(title="Title 1", author="Author 1", weight=10, cost=20),
            Book(title="Title 2", author="Author 2", weight=20, cost=30),
            Book(title="Title 3", author="Author 1", weight=15, cost=25)
        ]

    def test_save_load_state(self):
        storage = MagicMock(spec=StorageInterface)
        filename = "test_portfolio_state.mock"
        expected_data = {
            'max_weight': self.bookcase._max_weight,
            'books': [
                self.books[0]._asdict(),
                self.books[1]._asdict()
            ]
        }

        self.bookcase.add_book(self.books[0])
        self.bookcase.add_book(self.books[1])

        self.bookcase.save_state(storage, filename)
        storage.save.assert_called_once_with(expected_data, filename)

        new_bookcase = Bookcase(max_weight=100)
        storage.load.return_value = expected_data
        new_bookcase.load_state(storage, filename)

        self.assertEqual(len(new_bookcase._books), 2)
        self.assertEqual(new_bookcase._books[0], self.books[0])
        self.assertEqual(new_bookcase._books[1], self.books[1])


    def test_add_book(self):
        self.bookcase.add_book(self.books[0])
        self.assertEqual(len(self.bookcase._books), 1)
        self.assertEqual(self.bookcase.total_weight, 10)
        self.assertEqual(self.bookcase.total_cost, 20)

    def test_remove_book(self):
        self.bookcase.add_book(self.books[0])
        self.bookcase.add_book(self.books[1])
        self.bookcase.remove_book(self.books[0])
        self.assertEqual(self.bookcase.books_count, 1)
        self.assertEqual(self.bookcase.total_weight, 20)
        self.assertEqual(self.bookcase.total_cost, 30)

    def test_find_books_by_author(self):
        self.bookcase.add_book(self.books[0])
        self.bookcase.add_book(self.books[1])
        self.bookcase.add_book(self.books[2])
        books_by_author_1 = self.bookcase.find_books_by_author("Author 1")
        self.assertEqual(len(books_by_author_1), 2)
        self.assertEqual(books_by_author_1[0].title, "Title 1")
        self.assertEqual(books_by_author_1[1].title, "Title 3")

    def test_max_weight_exceeded(self):
        with self.assertRaises(MaxWeightExceededError):
            for i in range(5):
                self.bookcase.add_book(self.books[0])
                self.bookcase.add_book(self.books[1])

    def test_book_not_found(self):
        with self.assertRaises(BookNotFoundError):
            self.bookcase.remove_book(self.books[0])


if __name__ == '__main__':
    unittest.main()
