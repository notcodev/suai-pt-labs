import unittest

from main import User


class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = User(name="John Doe", age=30, gender="Male", address="123 Main St", phone="123-456-7890")

    def test_immutable_attributes(self):
        with self.assertRaises(AttributeError):
            self.user.name = "Jane Doe"
        with self.assertRaises(AttributeError):
            self.user.age = 31
        with self.assertRaises(AttributeError):
            self.user.gender = "Female"
        with self.assertRaises(AttributeError):
            self.user.address = "456 Second St"

    def test_mutable_attribute(self):
        self.user.phone = "123-456-789"
        self.assertEqual(self.user.phone, "123-456-789")


if __name__ == "__main__":
    unittest.main()
