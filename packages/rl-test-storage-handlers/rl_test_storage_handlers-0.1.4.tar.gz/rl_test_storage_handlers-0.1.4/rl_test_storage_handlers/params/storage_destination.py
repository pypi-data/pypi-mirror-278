from abc import ABC, abstractmethod
from typing import Any


class StorageDestination(ABC):
    @abstractmethod
    def get(self) -> Any:
        pass
