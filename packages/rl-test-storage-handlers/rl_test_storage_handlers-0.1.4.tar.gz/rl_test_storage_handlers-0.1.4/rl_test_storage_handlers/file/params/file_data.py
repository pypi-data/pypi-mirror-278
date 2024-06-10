from ...params.storage_data import StorageData


class FileData(StorageData):
    __data: str = ''

    def __init__(self, data: str) -> None:
        self.__data = data

    def get(self) -> str:
        return self.__data
