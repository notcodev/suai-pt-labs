from abc import ABC, abstractmethod
from typing import Any, Dict
import json

class StorageInterface(ABC):
    @abstractmethod
    def save(self, data: Dict[str, Any], filename: str) -> None:
        pass

    @abstractmethod
    def load(self, filename: str) -> Dict[str, Any]:
        pass
