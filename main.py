from typing import NamedTuple

class MaxWeightLimitError(Exception):
    """Исключение вызывается, когда достигнут максимальный вес."""
    pass


class ImbalanceLimitError(Exception):
    """Исключение вызывается, когда превышен лимит дисбаланса."""
    pass


class ParkingPlacesLimitError(Exception):
    """Исключение вызывается, когда на парковке не осталось свободных мест."""
    pass


class InvalidTicketError(Exception):
    """Исключение вызывается при попытке использования несуществующего билета."""
    pass


class Plate(NamedTuple):
    weight: int


class Vulture:
    def __init__(self, max_weight: int) -> None:
        self._max_weight = max_weight
        self._left_weight = 0
        self._right_weight = 0
        self._left_side = []
        self._right_side = []

    @property
    def total_weight(self) -> int:
        return self._left_weight + self._right_weight

    @property
    def weight_diff(self) -> int:
        return abs(self._left_weight - self._right_weight)

    def append_right(self, plate: Plate) -> None:
        if self.total_weight + plate.weight > self._max_weight:
            raise MaxWeightLimitError("Max weight limit reached")

        if abs(self._right_weight + plate.weight - self._left_weight) >= 20:
            raise ImbalanceLimitError("Imbalance limit reached")

        self._right_side.append(plate)
        self._right_weight += plate.weight

    def append_left(self, plate: Plate) -> None:
        if self.total_weight + plate.weight > self._max_weight:
            raise MaxWeightLimitError("Max weight limit reached")

        if abs(self._left_weight + plate.weight - self._right_weight) >= 20:
            raise ImbalanceLimitError("Imbalance limit reached")

        self._left_side.append(plate)
        self._left_weight += plate.weight

    def display(self) -> None:
        print("Левая сторона: ", self._left_side, "\n", "Правая сторона: ", self._right_side)


class Car(NamedTuple):
    manufacturer: str
    model: str
    gov_number: str


class Parking:
    def __init__(self, places: int) -> None:
        self._last_ticket = 0
        self._places = places
        self._cars: dict[int, Car] = {}

    @property
    def occupied_count(self) -> int:
        return len(self._cars.keys())

    def drive_in(self, car: Car) -> int:
        if self.occupied_count == self._places:
            raise ParkingPlacesLimitError("Places limit reached")

        ticket = self._last_ticket + 1

        self._cars[ticket] = car
        self._last_ticket = ticket

        return ticket

    def drive_out(self, ticket: int) -> Car:
        if ticket not in self._cars.keys():
            raise InvalidTicketError("Sorry, your car was already drived out")

        return self._cars.pop(ticket)

    def find(self, gov_number: str) -> Car | None:
        for car in self._cars.values():
            if car.gov_number == gov_number:
                return car

        return None

    def display(self):
        print(self._cars.values())
