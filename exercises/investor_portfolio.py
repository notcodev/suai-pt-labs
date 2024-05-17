from typing import NamedTuple, List, Dict, Union, Literal

from storages.interface import StorageInterface

class Asset(NamedTuple):
    type: Literal['STOCK'] | Literal['BOND']
    name: str
    price: float
    currency: str
    company: str

class InvestorPortfolio:
    def __init__(self):
        self.assets: List[Asset] = []

    def add_asset(self, asset: Asset) -> None:
        self.assets.append(asset)

    def total_value(self, currency: str, exchange_rates: Dict[str, Dict[str, float]]) -> float:
        total_value = 0
        for asset in self.assets:
            if asset.currency != currency:
                value_in_currency = asset.price * exchange_rates[asset.currency][currency]
            else:
                value_in_currency = asset.price
            total_value += value_in_currency
        return total_value

    def save_state(self, storage: StorageInterface, filename: str) -> None:
        data = {'assets': [asset._asdict() for asset in self.assets]}
        storage.save(data, filename)

    def load_state(self, storage: StorageInterface, filename: str) -> None:
        data = storage.load(filename)
        self.assets = [Asset(**asset) for asset in data['assets']]
