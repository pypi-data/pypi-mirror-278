from dbnomics_data_model.errors import DataModelError
from dbnomics_data_model.model import DatasetId
from dbnomics_data_model.validation.errors.validation_error_code_registry import ValidationErrorCodeRegistry
from dbnomics_data_model.validation.errors.validation_error_data import ValidationErrorData

CT001 = ValidationErrorCodeRegistry.register(
    "CT001", description="A dataset is referenced by the category tree but was not found in storage"
)
CT002 = ValidationErrorCodeRegistry.register(
    "CT002", description="A dataset was found in storage but is not referenced by the category tree"
)


class DanglingCategoryTreeDatasetReference(DataModelError):
    def __init__(self, dataset_id: DatasetId) -> None:
        msg = f"The dataset {str(dataset_id)!r} is referenced by the category tree but was not found in storage"
        super().__init__(msg=msg)
        self.dataset_id = dataset_id

    __validation_error_code__ = CT001

    @property
    def __validation_error_data__(self) -> ValidationErrorData:
        return ValidationErrorData(
            code=self.__validation_error_code__,
            path=self.dataset_id.validation_error_path,
        )


class DatasetMissingFromCategoryTree(DataModelError):
    def __init__(self, dataset_id: DatasetId) -> None:
        msg = f"The dataset {str(dataset_id)!r} was found in storage but is not referenced by the category tree"
        super().__init__(msg=msg)
        self.dataset_id = dataset_id

    __validation_error_code__ = CT002

    @property
    def __validation_error_data__(self) -> ValidationErrorData:
        return ValidationErrorData(
            code=self.__validation_error_code__,
            path=self.dataset_id.validation_error_path,
        )
