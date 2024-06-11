from pathlib import Path
from typing import TYPE_CHECKING

from dbnomics_data_model.model import DatasetCode
from dbnomics_data_model.storage.adapters.filesystem.constants import DATASET_JSON
from dbnomics_data_model.storage.adapters.filesystem.errors import FileSystemAdapterError

if TYPE_CHECKING:
    from dbnomics_data_model.storage.adapters.filesystem.model.base_dataset_json import BaseDatasetJson


class DatasetDirectoryManagerError(FileSystemAdapterError):
    pass


class DatasetJsonCodeMismatch(DatasetDirectoryManagerError):
    def __init__(self, *, dataset_json: "BaseDatasetJson", expected_dataset_code: DatasetCode) -> None:
        msg = f"Expected dataset code {str(expected_dataset_code)!r} but {DATASET_JSON} has {dataset_json.code!r}"
        super().__init__(msg=msg)
        self.dataset_json = dataset_json
        self.expected_dataset_code = expected_dataset_code


class DatasetDirectoryNameMismatch(DatasetDirectoryManagerError):
    def __init__(self, *, dataset_code: DatasetCode, dataset_dir: Path) -> None:
        msg = f"Expected dataset directory name to be the dataset code {str(dataset_code)!r}, but got {dataset_dir.name!r}"  # noqa: E501
        super().__init__(msg=msg)
        self.dataset_code = dataset_code
        self.dataset_dir = dataset_dir
