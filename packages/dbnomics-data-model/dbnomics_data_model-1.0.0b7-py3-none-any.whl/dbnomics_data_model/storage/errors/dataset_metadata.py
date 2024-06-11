from dbnomics_data_model.errors import DataModelError
from dbnomics_data_model.model import DatasetId, DatasetMetadata
from dbnomics_data_model.model.revisions.types import RevisionId
from dbnomics_data_model.validation.errors.validation_error_code_registry import ValidationErrorCodeRegistry
from dbnomics_data_model.validation.errors.validation_error_data import ValidationErrorData

DM001 = ValidationErrorCodeRegistry.register("DM001", description="Error loading metadata of a dataset")


class DatasetMetadataStorageError(DataModelError):
    def __init__(self, *, dataset_id: DatasetId, msg: str) -> None:
        super().__init__(msg=msg)
        self.dataset_id = dataset_id


class DatasetMetadataDeleteError(DatasetMetadataStorageError):
    def __init__(self, *, dataset_id: DatasetId) -> None:
        msg = f"Error deleting metadata of dataset {str(dataset_id)!r}"
        super().__init__(dataset_id=dataset_id, msg=msg)


class DatasetMetadataLoadError(DatasetMetadataStorageError):
    def __init__(self, *, dataset_id: DatasetId, revision_id: RevisionId | None) -> None:
        msg = f"Error loading metadata of dataset {str(dataset_id)!r}"
        super().__init__(dataset_id=dataset_id, msg=msg)
        self.revision_id = revision_id

    __validation_error_code__ = DM001

    @property
    def __validation_error_data__(self) -> ValidationErrorData:
        path = self.dataset_id.validation_error_path
        if self.revision_id is not None:
            path.append(("revision_id", self.revision_id))
        return ValidationErrorData(code=self.__validation_error_code__, path=path)


class DatasetMetadataNotFound(DatasetMetadataStorageError):
    def __init__(self, *, dataset_id: DatasetId, revision_id: RevisionId | None) -> None:
        msg = f"Could not find metadata of dataset {str(dataset_id)!r} at revision {revision_id!r}"
        super().__init__(dataset_id=dataset_id, msg=msg)
        self.revision_id = revision_id


class DatasetMetadataSaveError(DatasetMetadataStorageError):
    def __init__(self, *, dataset_id: DatasetId, dataset_metadata: DatasetMetadata) -> None:
        msg = f"Error saving metadata of dataset {str(dataset_id)!r}"
        super().__init__(dataset_id=dataset_id, msg=msg)
        self.dataset_metadata = dataset_metadata
