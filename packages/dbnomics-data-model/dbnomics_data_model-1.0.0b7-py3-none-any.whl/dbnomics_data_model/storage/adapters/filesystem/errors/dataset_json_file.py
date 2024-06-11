from pathlib import Path

from dbnomics_data_model.model import DatasetId
from dbnomics_data_model.model.revisions.types import RevisionId
from dbnomics_data_model.storage.adapters.filesystem.errors import FileSystemAdapterError


class DatasetJsonFileError(FileSystemAdapterError):
    def __init__(self, *, dataset_id: DatasetId, dataset_json_path: Path, msg: str) -> None:
        super().__init__(msg=msg)
        self.dataset_id = dataset_id
        self.dataset_json_path = dataset_json_path


class DatasetJsonDeleteError(DatasetJsonFileError):
    def __init__(self, *, dataset_id: DatasetId, dataset_json_path: Path) -> None:
        msg = f"Error deleting {dataset_json_path} of dataset {str(dataset_id)!r}"
        super().__init__(dataset_id=dataset_id, dataset_json_path=dataset_json_path, msg=msg)


class DatasetJsonLoadError(DatasetJsonFileError):
    def __init__(
        self, *, dataset_id: DatasetId, dataset_json_path: Path, revision_id: RevisionId | None = None
    ) -> None:
        msg = f"Error loading {dataset_json_path} of dataset {str(dataset_id)!r} at revision {revision_id!r}"
        super().__init__(dataset_id=dataset_id, dataset_json_path=dataset_json_path, msg=msg)
        self.revision_id = revision_id


class DatasetJsonNotFound(DatasetJsonFileError):
    def __init__(
        self, *, dataset_id: DatasetId, dataset_json_path: Path, revision_id: RevisionId | None = None
    ) -> None:
        msg = f"Could not find {dataset_json_path} of dataset {str(dataset_id)!r} at revision {revision_id!r}"
        super().__init__(dataset_id=dataset_id, dataset_json_path=dataset_json_path, msg=msg)
        self.revision_id = revision_id


class DatasetJsonSaveError(DatasetJsonFileError):
    def __init__(self, *, dataset_id: DatasetId, dataset_json_path: Path) -> None:
        msg = f"Error saving {dataset_json_path} of dataset {str(dataset_id)!r}"
        super().__init__(dataset_id=dataset_id, dataset_json_path=dataset_json_path, msg=msg)
