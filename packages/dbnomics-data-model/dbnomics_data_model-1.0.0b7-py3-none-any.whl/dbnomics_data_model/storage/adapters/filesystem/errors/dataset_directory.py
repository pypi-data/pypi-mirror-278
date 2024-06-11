from pathlib import Path

from dbnomics_data_model.model import DatasetId
from dbnomics_data_model.storage.adapters.filesystem.errors import FileSystemAdapterError


class DatasetDirectoryError(FileSystemAdapterError):
    def __init__(self, *, dataset_dir: Path, dataset_id: DatasetId, msg: str) -> None:
        super().__init__(msg=msg)
        self.dataset_dir = dataset_dir
        self.dataset_id = dataset_id


class DatasetDirectoryCreateError(DatasetDirectoryError):
    def __init__(self, *, dataset_dir: Path, dataset_id: DatasetId) -> None:
        msg = f"Error creating the directory of dataset {str(dataset_id)!r}: {dataset_dir}"
        super().__init__(dataset_dir=dataset_dir, dataset_id=dataset_id, msg=msg)


class DatasetDirectoryDeleteError(DatasetDirectoryError):
    def __init__(self, *, dataset_dir: Path, dataset_id: DatasetId) -> None:
        msg = f"Error deleting the directory of dataset {str(dataset_id)!r}: {dataset_dir}"
        super().__init__(dataset_dir=dataset_dir, dataset_id=dataset_id, msg=msg)


class DatasetDirectoryNotFound(DatasetDirectoryError):
    def __init__(self, *, dataset_dir: Path, dataset_id: DatasetId) -> None:
        msg = f"Could not find the directory of dataset {str(dataset_id)!r}: {dataset_dir}"
        super().__init__(dataset_dir=dataset_dir, dataset_id=dataset_id, msg=msg)
