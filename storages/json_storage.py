import json
from typing import Any, Dict
from .interface import StorageInterface


class JsonStorage(StorageInterface):
    def save(self, data: Dict[str, Any], filename: str) -> None:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)

    def load(self, filename: str) -> Dict[str, Any]:
        with open(filename, 'r') as file:
            return json.load(file)
