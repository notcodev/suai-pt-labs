import unittest
from .bookcase import Book, Bookcase, MaxWeightExceededError, BookNotFoundError
from storages.txt_storage import TxtStorage


class TestBookcase(unittest.TestCase):
    def setUp(self):
        self.bookcase = Bookcase(max_weight=100)
        self.book1 = Book(title="Title 1", author="Author 1", weight=10, cost=20)
        self.book2 = Book(title="Title 2", author="Author 2", weight=20, cost=30)
        self.book3 = Book(title="Title 3", author="Author 1", weight=15, cost=25)

    def test_save_load_state(self):
        storage = TxtStorage()

        self.bookcase.add_book(self.book1)
        self.bookcase.add_book(self.book2)

        filename = "test_state.txt"
        self.bookcase.save_state(storage, filename)

        self.bookcase = Bookcase(max_weight=self.bookcase._max_weight)

        self.bookcase.load_state(storage, filename)

        self.assertEqual(len(self.bookcase._books), 2)
        self.assertEqual(self.bookcase._books[0], self.book1)
        self.assertEqual(self.bookcase._books[1], self.book2)

    def test_add_book(self):
        self.bookcase.add_book(self.book1)
        self.assertEqual(len(self.bookcase._books), 1)
        self.assertEqual(self.bookcase.total_weight, 10)
        self.assertEqual(self.bookcase.total_cost, 20)

    def test_remove_book(self):
        self.bookcase.add_book(self.book1)
        self.bookcase.add_book(self.book2)
        self.bookcase.remove_book(self.book1)
        self.assertEqual(self.bookcase.books_count, 1)
        self.assertEqual(self.bookcase.total_weight, 20)
        self.assertEqual(self.bookcase.total_cost, 30)

    def test_find_books_by_author(self):
        self.bookcase.add_book(self.book1)
        self.bookcase.add_book(self.book2)
        self.bookcase.add_book(self.book3)
        books_by_author_1 = self.bookcase.find_books_by_author("Author 1")
        self.assertEqual(len(books_by_author_1), 2)
        self.assertEqual(books_by_author_1[0].title, "Title 1")
        self.assertEqual(books_by_author_1[1].title, "Title 3")

    def test_max_weight_exceeded(self):
        with self.assertRaises(MaxWeightExceededError):
            for i in range(5):
                self.bookcase.add_book(self.book1)
                self.bookcase.add_book(self.book2)

    def test_book_not_found(self):
        with self.assertRaises(BookNotFoundError):
            self.bookcase.remove_book(self.book1)


if __name__ == '__main__':
    unittest.main()
