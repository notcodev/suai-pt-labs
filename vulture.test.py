import unittest
from main import ImbalanceLimitError, MaxWeightLimitError, Vulture, Plate

class TestVulture(unittest.TestCase):
    def setUp(self) -> None:
        self.vulture = Vulture(max_weight=100)
        self.plate_10 = Plate(weight=10)
        self.plate_15 = Plate(weight=15)

    def test_append_left(self):
        # Добавление тарелки на левую сторону
        self.vulture.append_left(self.plate_10)
        self.assertEqual(self.vulture._left_weight, 10)
        self.assertEqual(len(self.vulture._left_side), 1)

    def test_append_right(self):
        # Добавление тарелки на правую сторону
        self.vulture.append_right(self.plate_15)
        self.assertEqual(self.vulture._right_weight, 15)
        self.assertEqual(len(self.vulture._right_side), 1)

    def test_total_weight(self):
        # Проверка общего веса
        self.vulture.append_left(self.plate_10)
        self.vulture.append_right(self.plate_15)
        self.assertEqual(self.vulture.total_weight, 25)

    def test_weight_diff(self):
        self.vulture.append_left(self.plate_10)
        self.vulture.append_right(self.plate_15)
        self.assertEqual(self.vulture.weight_diff, 5)

    def test_max_weight_limit(self):
        with self.assertRaises(MaxWeightLimitError):
            for _ in range(11):
                self.vulture.append_right(Plate(weight=10))

    def test_imbalance_limit(self):
        self.vulture.append_left(Plate(weight=10))
        with self.assertRaises(ImbalanceLimitError):
            self.vulture.append_right(Plate(weight=30))

if __name__ == "__main__":
    unittest.main()
