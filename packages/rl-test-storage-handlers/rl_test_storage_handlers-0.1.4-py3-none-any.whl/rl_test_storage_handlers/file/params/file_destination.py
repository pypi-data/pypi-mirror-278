from ...params.storage_destination import StorageDestination


class FileDestination(StorageDestination):
    __file_name: str = ''

    def __init__(self, file_name: str) -> None:
        self.__file_name = file_name

    def get(self) -> str:
        return self.__file_name
