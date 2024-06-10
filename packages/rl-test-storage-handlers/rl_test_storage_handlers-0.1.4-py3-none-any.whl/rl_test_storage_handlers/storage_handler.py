from abc import ABC, abstractmethod

from .params.storage_data import StorageData
from .params.storage_destination import StorageDestination


class StorageHandler(ABC):
    @abstractmethod
    def write(self, destination: StorageDestination, data: StorageData) -> None:
        pass

    @abstractmethod
    def read(self, destination: StorageDestination) -> StorageData:
        pass
