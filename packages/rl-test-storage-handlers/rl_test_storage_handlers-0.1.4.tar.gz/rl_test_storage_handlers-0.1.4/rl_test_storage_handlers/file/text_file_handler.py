from .file_handler import FileHandler
from .params.file_data import FileData
from .params.file_destination import FileDestination


class TextFileHandler(FileHandler):
    def write(self, destination: FileDestination, data: FileData) -> None:
        return super()._write(destination, 'w', data)

    def read(self, destination: FileDestination) -> FileData:
        return super()._read(destination, 'r')
