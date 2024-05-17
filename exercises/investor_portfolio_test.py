import unittest
from unittest.mock import MagicMock
from .investor_portfolio import InvestorPortfolio, Asset
from storages.interface import StorageInterface

class TestInvestorPortfolio(unittest.TestCase):
    def setUp(self):
        self.portfolio = InvestorPortfolio()
        self.stock = Asset(type='STOCK', name="Sberbank", price=100, currency="RUB", company="Sberbank")
        self.bond = Asset(type='BOND', name="Government bond", price=500, currency="USD", company="Government")

    def test_add_asset(self):
        self.assertEqual(len(self.portfolio.assets), 0)
        self.portfolio.add_asset(self.stock)
        self.assertEqual(len(self.portfolio.assets), 1)
        self.assertEqual(self.portfolio.assets[0], self.stock)

    def test_total_value(self):
        self.portfolio.add_asset(self.stock)
        self.portfolio.add_asset(self.bond)

        exchange_rates = {
            "RUB": {"USD": 0.015},
            "USD": {"RUB": 66.67}
        }
        total_value_rub = self.portfolio.total_value(currency="RUB", exchange_rates=exchange_rates)
        total_value_usd = self.portfolio.total_value(currency="USD", exchange_rates=exchange_rates)

        self.assertAlmostEqual(total_value_rub, 100 + 500 * 66.67, delta=0.01)
        self.assertAlmostEqual(total_value_usd, 100 / 66.67 + 500, delta=0.01)

    def test_save_load_state(self):
        storage = MagicMock(spec=StorageInterface)
        filename = "test_portfolio_state.json"
        expected_data = {'assets': [self.stock._asdict(), self.bond._asdict()]}

        self.portfolio.add_asset(self.stock)
        self.portfolio.add_asset(self.bond)

        self.portfolio.save_state(storage, filename)
        storage.save.assert_called_once_with(expected_data, filename)

        self.portfolio = InvestorPortfolio()
        storage.load.return_value = expected_data

        self.portfolio.load_state(storage, filename)
        storage.load.assert_called_once_with(filename)

        self.assertEqual(len(self.portfolio.assets), 2)
        self.assertEqual(self.portfolio.assets[0], self.stock)
        self.assertEqual(self.portfolio.assets[1], self.bond)

if __name__ == '__main__':
    unittest.main()
