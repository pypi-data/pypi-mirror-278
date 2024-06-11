from typing import TYPE_CHECKING, cast

from jsonalias import Json

from dbnomics_data_model.storage.adapters.filesystem.constants import DATASET_JSON
from dbnomics_data_model.storage.adapters.filesystem.errors.json_model import JsonModelError
from dbnomics_data_model.validation.errors.validation_error_code_registry import ValidationErrorCodeRegistry
from dbnomics_data_model.validation.errors.validation_error_data import ValidationErrorData

if TYPE_CHECKING:
    from dbnomics_data_model.storage.adapters.filesystem.model.base_dataset_json import BaseDatasetJson


DJ001 = ValidationErrorCodeRegistry.register(
    "DJ001", description="Some keys of 'dimensions_labels' are not present in 'dimensions_codes_order'"
)
DJ002 = ValidationErrorCodeRegistry.register(
    "DJ002", description="Some keys of 'dimensions_values_labels' are not present in 'dimensions_codes_order'"
)


class DatasetJsonError(JsonModelError):
    def __init__(self, *, dataset_json: "BaseDatasetJson", msg: str) -> None:
        super().__init__(msg=msg)
        self.dataset_json = dataset_json


class DimensionValueCreateError(DatasetJsonError):
    def __init__(self, *, dataset_json: "BaseDatasetJson", dimension_code: str, dimension_value_code: str) -> None:
        msg = f"Could not create a DimensionValue instance from {DATASET_JSON!r} for dimension {dimension_code!r}={dimension_value_code!r}"  # noqa: E501
        super().__init__(dataset_json=dataset_json, msg=msg)


class UnusedDimensionLabelsKeys(DatasetJsonError):
    def __init__(self, *, dataset_json: "BaseDatasetJson", unused_dimension_codes: set[str]) -> None:
        msg = "Some keys of 'dimensions_labels' are not present in 'dimensions_codes_order'"
        super().__init__(dataset_json=dataset_json, msg=msg)
        self.unused_dimension_codes = unused_dimension_codes

    __validation_error_code__ = DJ001

    @property
    def __validation_error_data__(self) -> ValidationErrorData:
        unused_dimension_codes_json = cast(Json, sorted(self.unused_dimension_codes))
        return ValidationErrorData(
            code=self.__validation_error_code__,
            extra={"unused_dimension_codes": unused_dimension_codes_json},
            path=[("dataset_code", self.dataset_json.code)],
        )


class UnusedDimensionValueLabelsKeys(DatasetJsonError):
    def __init__(self, *, dataset_json: "BaseDatasetJson", unused_dimension_codes: set[str]) -> None:
        msg = "Some keys of 'dimensions_values_labels' are not present in 'dimensions_codes_order'"
        super().__init__(dataset_json=dataset_json, msg=msg)
        self.unused_dimension_codes = unused_dimension_codes

    __validation_error_code__ = DJ002

    @property
    def __validation_error_data__(self) -> ValidationErrorData:
        unused_dimension_codes_json = cast(Json, sorted(self.unused_dimension_codes))
        return ValidationErrorData(
            code=self.__validation_error_code__,
            extra={"unused_dimension_codes": unused_dimension_codes_json},
            path=[("dataset_code", self.dataset_json.code)],
        )
