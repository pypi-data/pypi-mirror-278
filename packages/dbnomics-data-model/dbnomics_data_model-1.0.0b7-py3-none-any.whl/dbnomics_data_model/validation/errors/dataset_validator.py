from typing import cast

from jsonalias import Json

from dbnomics_data_model.errors import DataModelError
from dbnomics_data_model.model import DatasetId, SeriesCode
from dbnomics_data_model.validation.errors.validation_error_code_registry import ValidationErrorCodeRegistry
from dbnomics_data_model.validation.errors.validation_error_data import ValidationErrorData

D001 = ValidationErrorCodeRegistry.register("D001", description="A dataset has many series with the same code")
D002 = ValidationErrorCodeRegistry.register("D002", description="A dataset has many series with the same name")


class DuplicateSeriesCode(DataModelError):
    def __init__(self, *, count: int, dataset_id: DatasetId, series_code: SeriesCode) -> None:
        msg = f"The dataset {str(dataset_id)!r} has {count} series with the same code {series_code!r}"
        super().__init__(msg=msg)
        self.count = count
        self.dataset_id = dataset_id
        self.series_code = series_code

    __validation_error_code__ = D001

    @property
    def __validation_error_data__(self) -> ValidationErrorData:
        return ValidationErrorData(
            code=self.__validation_error_code__,
            extra={
                "count": self.count,
                "series_code": self.series_code,
            },
            path=self.dataset_id.validation_error_path,
        )


class DuplicateSeriesName(DataModelError):
    def __init__(self, *, dataset_id: DatasetId, series_name: str, series_codes: set[SeriesCode]) -> None:
        count = len(series_codes)
        msg = f"The dataset {str(dataset_id)!r} has {count} series with the same name {series_name!r}"
        super().__init__(msg=msg)
        self.dataset_id = dataset_id
        self.series_codes = series_codes
        self.series_name = series_name

    __validation_error_code__ = D002

    @property
    def __validation_error_data__(self) -> ValidationErrorData:
        series_codes_json = cast(Json, sorted(self.series_codes))
        return ValidationErrorData(
            code=self.__validation_error_code__,
            extra={
                "series_codes": series_codes_json,
                "series_name": self.series_name,
            },
            path=self.dataset_id.validation_error_path,
        )
