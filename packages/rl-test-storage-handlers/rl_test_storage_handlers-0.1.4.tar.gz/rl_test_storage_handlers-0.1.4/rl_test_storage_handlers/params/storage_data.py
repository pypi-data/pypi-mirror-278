from abc import ABC, abstractmethod
from typing import Any


class StorageData(ABC):
    @abstractmethod
    def get(self) -> Any:
        pass
