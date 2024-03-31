import unittest
from main import InvalidTicketError, Parking, Car, ParkingPlacesLimitError

class TestParking(unittest.TestCase):
    def setUp(self) -> None:
        self.parking = Parking(places=2)
        self.car1 = Car(manufacturer="Toyota", model="Camry", gov_number="A111AA777")
        self.car2 = Car(manufacturer="BMW", model="X5", gov_number="B222BB888")

    def test_drive_in(self):
        ticket = self.parking.drive_in(self.car1)
        self.assertEqual(ticket, 1)
        self.assertEqual(self.parking.occupied_count, 1)

    def test_parking_limit(self):
        self.parking.drive_in(self.car1)
        self.parking.drive_in(self.car2)
        with self.assertRaises(ParkingPlacesLimitError):
            self.parking.drive_in(Car(manufacturer="Nissan", model="Almera", gov_number="C333CC999"))

    def test_drive_out(self):
        ticket = self.parking.drive_in(self.car1)
        car = self.parking.drive_out(ticket)
        self.assertEqual(car, self.car1)
        self.assertEqual(self.parking.occupied_count, 0)

    def test_drive_out_nonexistent_ticket(self):
            # Попытка выгнать машину по несуществующему билету
            self.parking.drive_in(self.car1)
            with self.assertRaises(InvalidTicketError):
                self.parking.drive_out(999)

    def test_find_car(self):
        self.parking.drive_in(self.car1)
        found_car = self.parking.find(self.car1.gov_number)
        self.assertEqual(found_car, self.car1)

    def test_car_not_found(self):
        self.parking.drive_in(self.car1)
        found_car = self.parking.find("D444DD010")
        self.assertIsNone(found_car)

if __name__ == "__main__":
    unittest.main()
