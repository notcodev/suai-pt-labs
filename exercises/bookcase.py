import sys
from dataclasses import dataclass
from typing import NamedTuple

from storages.interface import StorageInterface


class BookcaseError(Exception):
    """Базовый класс для всех исключений книжного шкафа."""
    pass

class MaxWeightExceededError(BookcaseError):
    """Исключение, возникающее при попытке добавить книгу, превышающую максимальный вес."""
    pass

class BookNotFoundError(BookcaseError):
    """Исключение, возникающее, когда запрашиваемая книга не найдена."""
    pass


class Book(NamedTuple):
    title: str
    author: str
    weight: float
    cost: float


class Bookcase:
    def __init__(self, max_weight: float):
        self._max_weight = max_weight
        self._current_weight: float = 0
        self._current_cost: float = 0
        self._books: list[Book] = []

    def add_book(self, book: Book):
        if self._current_weight + book.weight > self._max_weight:
            raise MaxWeightExceededError('Unable to add: Max weight of bookcase exceeded')

        self._books.append(book)
        self._current_weight += book.weight
        self._current_cost += book.cost

    def remove_book(self, book: Book):
        if book not in self._books:
            raise BookNotFoundError('Unable to remove: Book not fonud')

        self._books.remove(book)
        self._current_weight -= book.weight
        self._current_cost -= book.cost

    def find_books_by_author(self, author: str) -> list[Book]:
        return [book for book in self._books if book.author == author]

    @property
    def total_weight(self) -> float:
        return self._current_weight

    @property
    def total_cost(self) -> float:
        return self._current_cost

    @property
    def books_count(self) -> int:
        return len(self._books)

    def save_state(self, storage: StorageInterface, filename: str):
        data = {
            "max_weight": self._max_weight,
            "books": [
                {"title": book.title, "author": book.author, "weight": book.weight, "cost": book.cost}
                for book in self._books
            ]
        }
        storage.save(data, filename)

    def load_state(self, storage: StorageInterface, filename: str):
        data = storage.load(filename)
        self._max_weight = data["max_weight"]
        self._books = [
            Book(title=book["title"], author=book["author"], weight=book["weight"], cost=book["cost"])
            for book in data["books"]
        ]
