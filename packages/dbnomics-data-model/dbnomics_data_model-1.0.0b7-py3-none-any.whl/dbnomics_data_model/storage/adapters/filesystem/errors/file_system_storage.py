from pathlib import Path

from dbnomics_data_model.storage.adapters.filesystem.errors import FileSystemAdapterError


class StorageDirectoryNotFound(FileSystemAdapterError):
    def __init__(self, *, storage_dir: Path) -> None:
        msg = f"Could not find the storage directory {str(storage_dir)!r}"
        super().__init__(msg=msg)
        self.storage_dir = storage_dir
