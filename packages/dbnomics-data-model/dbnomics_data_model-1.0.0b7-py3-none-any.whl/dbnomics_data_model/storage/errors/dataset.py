from dbnomics_data_model.errors import DataModelError
from dbnomics_data_model.model import DatasetId
from dbnomics_data_model.model.revisions.types import RevisionId


class DatasetStorageError(DataModelError):
    def __init__(self, *, dataset_id: DatasetId, msg: str) -> None:
        super().__init__(msg=msg)
        self.dataset_id = dataset_id


class DatasetDeleteError(DatasetStorageError):
    def __init__(self, *, dataset_id: DatasetId) -> None:
        msg = f"Error deleting dataset {str(dataset_id)!r}"
        super().__init__(dataset_id=dataset_id, msg=msg)


class DatasetNotFound(DatasetStorageError):
    def __init__(self, *, dataset_id: DatasetId) -> None:
        msg = f"Could not find dataset {str(dataset_id)!r}"
        super().__init__(dataset_id=dataset_id, msg=msg)


class DatasetSomeSeriesDeleteError(DatasetStorageError):
    def __init__(self, *, dataset_id: DatasetId) -> None:
        msg = f"Error deleting some series from dataset {str(dataset_id)!r}"
        super().__init__(dataset_id=dataset_id, msg=msg)


class DatasetSomeSeriesLoadError(DatasetStorageError):
    def __init__(self, *, dataset_id: DatasetId, revision_id: RevisionId | None = None) -> None:
        msg = f"Error loading some series from dataset {str(dataset_id)!r} at revision {revision_id!r}"
        super().__init__(dataset_id=dataset_id, msg=msg)
        self.revision_id = revision_id


class DatasetSomeSeriesNotFound(DatasetStorageError):
    def __init__(self, *, dataset_id: DatasetId, revision_id: RevisionId | None = None) -> None:
        msg = f"Could not find series in dataset {str(dataset_id)!r} at revision {revision_id!r}"
        super().__init__(dataset_id=dataset_id, msg=msg)
        self.revision_id = revision_id


class DatasetSeriesLoadError(DatasetStorageError):
    def __init__(self, *, dataset_id: DatasetId, revision_id: RevisionId | None = None, series_code: str) -> None:
        msg = f"Error loading series {series_code!r} from dataset {str(dataset_id)!r} at revision {revision_id!r}"
        super().__init__(dataset_id=dataset_id, msg=msg)
        self.revision_id = revision_id
        self.series_code = series_code


class DatasetHasNoSeries(DatasetStorageError):
    def __init__(self, *, dataset_id: DatasetId) -> None:
        msg = f"Dataset {str(dataset_id)!r} has no series"
        super().__init__(dataset_id=dataset_id, msg=msg)


class DatasetSomeSeriesSaveError(DatasetStorageError):
    def __init__(self, *, dataset_id: DatasetId) -> None:
        msg = f"Error saving some series from dataset {str(dataset_id)!r}"
        super().__init__(dataset_id=dataset_id, msg=msg)
