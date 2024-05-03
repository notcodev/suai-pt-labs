from copyreg import constructor
from dataclasses import dataclass
from typing import Any, Dict, Iterable, Optional
from .interface import StorageInterface

class QueueEmptyError(Exception):
    """Исключение, вызываемое при попытке удалить элемент из пустой очереди."""
    pass


@dataclass
class QueueNode[T]:
    value: T
    next: 'QueueNode | None' = None


class Queue[T]:
    def __init__(self, iterable: Optional[Iterable[T]] = None) -> None:
        self._head: QueueNode | None = None
        self._tail: QueueNode | None = None
        self._lenght = 0

        if iterable is not None:
            for item in iterable:
                self.add(item)

    def __len__(self):
        return self._lenght

    def add(self, value: T) -> None:
        node = QueueNode(value=value)
        self._lenght += 1

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

        self._lenght -= 1

        return node.value


class TxtStorage(StorageInterface):
    def save(self, data: Dict[str, Any], filename: str) -> None:
        with open(filename, 'w') as file:
            queue = Queue[tuple[str, Any]]()

            for key, item in data.items():
                queue.add((f'{type(key).__name__}|{key}', item))

            while queue:
                main_key, item = queue.pop()

                if isinstance(item, list):
                    for index, element in enumerate(item):
                        queue.add((f'{main_key}|{type(item).__name__}:int|{index}', element))
                elif isinstance(item, dict):
                    for key, element in item.items():
                        if not isinstance(key, (str, int, bool, float)):
                            raise KeyError('TxtStorage supports only str, int, float and bool keys')
                        queue.add((f'{main_key}|dict:{type(key).__name__}|{key}', element))
                elif isinstance(item, (str, int, bool, float)):
                    file.write(f"{main_key}|{type(item).__name__}:{item}\n")
                else:
                    raise ValueError('TxtStorage supports only dict, list, str, int, float and bool values')

    def load(self, filename: str) -> Dict[str, Any]:
        data = {}
        classes = {"dict": dict, "list": list, "str": str, "int": int, "float": float, "bool": bool}
        with open(filename, 'r') as file:
            for line in file:
                *key_parts, value = line.strip().split(':')

                parent = data

                for index, key in enumerate(key_parts):
                    key_type, key_value, value_type = key.split('|')
                    typed_key = classes[key_type](key_value)
                    constructor = classes[value_type]

                    if isinstance(parent, list):
                        while typed_key >= len(parent):
                            parent.append(None)

                    if isinstance(parent, dict) and parent.get(typed_key, None) is None or isinstance(parent, list) and parent[typed_key] is None:
                        parent[typed_key] = constructor(value) if index == len(key_parts) - 1 else constructor()

                    parent = parent[typed_key]


        return data
