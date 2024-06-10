import logging
import os
from abc import abstractmethod

from dotenv import load_dotenv
from rl_test_common import Config

from ..params.storage_data import StorageData
from ..params.storage_destination import StorageDestination
from ..storage_handler import StorageHandler
from .params.file_data import FileData
from .params.file_destination import FileDestination

load_dotenv()


class FileHandler(StorageHandler):
    __logger: logging.Logger = logging.getLogger(__name__)

    __config: Config = Config(os.getenv('CONFIG_FILE_PATH'))

    @abstractmethod
    def write(self, destination: StorageDestination, data: StorageData) -> None:
        pass

    @abstractmethod
    def read(self, destination: StorageDestination) -> StorageData:
        pass

    def _write(self, destination: FileDestination, mode: str, data: FileData) -> None:
        file_path: str = self.__get_file_path(destination.get())

        with open(file_path, mode) as file:
            file.write(data.get())

    def _read(self, destination: FileDestination, mode: str) -> FileData:
        file_path: str = self.__get_file_path(destination.get())
        data: FileData = FileData('')

        try:
            with open(file_path, mode) as file:
                data = FileData(file.read())

        except FileNotFoundError:
            self.__logger.error(f'File not found: {file_path}.')

        return data

    def __get_file_path(self, file_name: str) -> str:
        return f'{self.__config.user_files_root_dir}/{file_name}'
