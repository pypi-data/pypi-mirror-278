from dbnomics_data_model.errors import DataModelError
from dbnomics_data_model.model.dataset_metadata import DatasetMetadata
from dbnomics_data_model.model.identifiers.dataset_code import DatasetCode


class DatasetMetadataModelError(DataModelError):
    def __init__(self, *, dataset_metadata: DatasetMetadata, msg: str) -> None:
        super().__init__(msg=msg)
        self.dataset_metadata = dataset_metadata


class DatasetMetadataCodeMismatch(DatasetMetadataModelError):
    def __init__(self, *, dataset_metadata: DatasetMetadata, expected_dataset_code: DatasetCode) -> None:
        msg = f"Expected dataset code {str(expected_dataset_code)!r} but model instance has {dataset_metadata.code!r}"
        super().__init__(msg=msg, dataset_metadata=dataset_metadata)
        self.expected_dataset_code = expected_dataset_code
