from dataclasses import dataclass
from typing import Literal


class QueueEmptyError(Exception):
    """Исключение, вызываемое при попытке удалить элемент из пустой очереди."""
    pass


@dataclass
class QueueNode[T]:
    value: T
    next: 'QueueNode[T] | None' = None


class Queue[T]:
    def __init__(self) -> None:
        self._head: QueueNode[T] | None = None
        self._tail: QueueNode[T] | None = None

    def add(self, value: T) -> None:
        node = QueueNode[T](value=value)

        if self._tail is None:
            self._head = node
            self._tail = node
            return

        self._tail.next = node
        self._tail = node

    def pop(self) -> T:
        if self._head is None:
            raise QueueEmptyError('Queue is empty')

        node = self._head
        self._head = self._head.next

        if self._head is None:
            self._tail = None

        return node.value


class User:
    _immutable_attributes = {'name', 'age', 'gender', 'address'}

    def __init__(self, name: str, age: int, gender: Literal['Male', 'Female'], address: str, phone: str):
        self.name = name
        self.age = age
        self.gender = gender
        self.address = address
        self.phone = phone

    def __setattr__(self, key, value):
        if key in self._immutable_attributes and hasattr(self, key):
            raise AttributeError(f"{key} is immutable and cannot be changed")
        else:
            super().__setattr__(key, value)
