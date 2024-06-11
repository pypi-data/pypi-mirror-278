from pathlib import Path

from dbnomics_data_model.storage.adapters.filesystem.errors import FileSystemAdapterError


class FileSystemStorageUriInitError(FileSystemAdapterError):
    pass


class NotADirectory(FileSystemStorageUriInitError):
    def __init__(self, path: Path) -> None:
        msg = f"{str(path)!r} is not a directory"
        super().__init__(msg=msg)
        self.path = path
