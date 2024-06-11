from typing import TYPE_CHECKING, cast

from jsonalias import Json

from dbnomics_data_model.errors import DataModelError
from dbnomics_data_model.model.frequency import Frequency
from dbnomics_data_model.model.identifiers.series_code_or_id import SeriesCodeOrId
from dbnomics_data_model.validation.errors.validation_error_code_registry import ValidationErrorCodeRegistry
from dbnomics_data_model.validation.errors.validation_error_data import ValidationErrorData

if TYPE_CHECKING:
    from dbnomics_data_model.model.dimensions.dataset_dimensions import DatasetDimensions
    from dbnomics_data_model.model.dimensions.dimension import Dimension
    from dbnomics_data_model.model.identifiers.dataset_id import DatasetId
    from dbnomics_data_model.model.identifiers.series_code import SeriesCode
    from dbnomics_data_model.model.identifiers.types import DimensionCode, DimensionValueCode

SD001 = ValidationErrorCodeRegistry.register(
    "SD001",
    description="A series uses a value for the frequency dimension that is not defined in dataset metadata",
)
SD002 = ValidationErrorCodeRegistry.register(
    "SD002", description="A series uses a dimension that is not defined in dataset metadata"
)
SD003 = ValidationErrorCodeRegistry.register(
    "SD003", description="A series uses a dimension value that is not defined in dataset metadata"
)


class SeriesInvalidFrequencyDimensionValue(DataModelError):
    def __init__(
        self,
        *,
        dataset_id: "DatasetId | None" = None,
        dimension_code: "DimensionCode",
        dimension_value_code: "DimensionValueCode",
        series_code: "SeriesCode",
    ) -> None:
        allowed_values = [frequency.value.code for frequency in Frequency]
        series_code_or_id = SeriesCodeOrId(series_code, dataset_id=dataset_id)
        msg = f"The series {str(series_code_or_id)!r} uses an invalid value {dimension_value_code!r} for the frequency dimension {dimension_code!r}, allowed values: {allowed_values!r}"  # noqa: E501
        super().__init__(msg=msg)
        self.allowed_values = allowed_values
        self.dataset_id = dataset_id
        self.dimension_code = dimension_code
        self.dimension_value_code = dimension_value_code
        self.series_code = series_code

    __validation_error_code__ = SD001

    @property
    def __validation_error_data__(self) -> ValidationErrorData:
        series_code_or_id = SeriesCodeOrId(self.series_code, dataset_id=self.dataset_id)
        return ValidationErrorData(
            code=self.__validation_error_code__,
            extra={
                "allowed_values": cast(list[Json], self.allowed_values),
                "dimension_code": self.dimension_code,
                "dimension_value_code": self.dimension_value_code,
            },
            path=series_code_or_id.validation_error_path,
        )


class SeriesUndefinedDimension(DataModelError):
    def __init__(
        self,
        *,
        dataset_dimensions: "DatasetDimensions",
        dataset_id: "DatasetId | None" = None,
        dimension_code: "DimensionCode",
        series_code: "SeriesCode",
    ) -> None:
        series_code_or_id = SeriesCodeOrId(series_code, dataset_id=dataset_id)
        msg = f"The series {str(series_code_or_id)!r} uses an invalid dimension {dimension_code!r}, allowed values: {dataset_dimensions.dimension_codes!r}"  # noqa: E501
        super().__init__(msg=msg)
        self.dataset_dimensions = dataset_dimensions
        self.dataset_id = dataset_id
        self.dimension_code = dimension_code
        self.series_code = series_code

    __validation_error_code__ = SD002

    @property
    def __validation_error_data__(self) -> ValidationErrorData:
        series_code_or_id = SeriesCodeOrId(self.series_code, dataset_id=self.dataset_id)
        return ValidationErrorData(
            code=self.__validation_error_code__,
            extra={"dimension_code": self.dimension_code},
            path=series_code_or_id.validation_error_path,
        )


class SeriesUndefinedDimensionValue(DataModelError):
    def __init__(
        self,
        *,
        dataset_id: "DatasetId | None" = None,
        dimension: "Dimension",
        dimension_value_code: "DimensionValueCode",
        series_code: "SeriesCode",
    ) -> None:
        series_code_or_id = SeriesCodeOrId(series_code, dataset_id=dataset_id)
        msg = f"The series {str(series_code_or_id)!r} uses an invalid value {dimension_value_code!r} for the dimension {dimension.code!r}, allowed values: {dimension.value_codes!r}"  # noqa: E501
        super().__init__(msg=msg)
        self.dataset_id = dataset_id
        self.dimension = dimension
        self.dimension_value_code = dimension_value_code
        self.series_code = series_code

    __validation_error_code__ = SD003

    @property
    def __validation_error_data__(self) -> ValidationErrorData:
        series_code_or_id = SeriesCodeOrId(self.series_code, dataset_id=self.dataset_id)
        return ValidationErrorData(
            code=self.__validation_error_code__,
            extra={
                "dimension_code": self.dimension.code,
                "dimension_value_code": self.dimension_value_code,
            },
            path=series_code_or_id.validation_error_path,
        )
