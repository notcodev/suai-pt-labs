from storages.interface import StorageInterface


class CupboardError(Exception):
    """Базовый класс для всех исключений шкафа."""
    pass


class InsufficientItemQuantityError(CupboardError):
    """Исключение, возникающее при попытке удалить больше предметов, чем есть."""
    pass


class Cupboard:
    def __init__(self):
        self.items: dict[str, int] = {}

    def add_item(self, item: str, quantity: int) -> None:
        if item in self.items:
            self.items[item] += quantity
        else:
            self.items[item] = quantity

    def remove_item(self, item: str, quantity: int) -> None:
        if item not in self.items or self.items[item] < quantity:
            raise InsufficientItemQuantityError(f'Unable to remove: there is no "{item}" with quantity>={quantity}')

        self.items[item] -= quantity
        if self.items[item] == 0:
            del self.items[item]

    def save_state(self, storage: StorageInterface, filename: str) -> None:
        storage.save(self.items, filename)

    def load_state(self, storage: StorageInterface, filename: str) -> None:
        self.items = storage.load(filename)
