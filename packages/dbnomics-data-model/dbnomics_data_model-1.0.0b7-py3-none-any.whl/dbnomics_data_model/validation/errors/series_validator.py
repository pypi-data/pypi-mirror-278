from typing import TYPE_CHECKING, cast

from jsonalias import Json

from dbnomics_data_model.errors import DataModelError
from dbnomics_data_model.model.identifiers.series_code_or_id import SeriesCodeOrId
from dbnomics_data_model.model.periods import Period
from dbnomics_data_model.validation.errors.validation_error_code_registry import ValidationErrorCodeRegistry
from dbnomics_data_model.validation.errors.validation_error_data import ValidationErrorData

if TYPE_CHECKING:
    from dbnomics_data_model.model.identifiers.dataset_id import DatasetId
    from dbnomics_data_model.model.identifiers.series_code import SeriesCode

SO001 = ValidationErrorCodeRegistry.register("SO001", description="Some series observations have the same period")
SO002 = ValidationErrorCodeRegistry.register("SO002", description="Series observation periods have inconsistent types")
SO003 = ValidationErrorCodeRegistry.register("SO003", description="Series observations are not sorted by period")


class DuplicateSeriesObservationPeriods(DataModelError):
    def __init__(
        self,
        *,
        dataset_id: "DatasetId | None" = None,
        duplicate_periods: dict[Period, int],
        series_code: "SeriesCode",
    ) -> None:
        series_code_or_id = SeriesCodeOrId(series_code, dataset_id=dataset_id)
        msg = f"Some observations of the series {str(series_code_or_id)!r} have the same period"
        super().__init__(msg=msg)
        self.dataset_id = dataset_id
        self.duplicate_periods = duplicate_periods
        self.series_code = series_code

    __validation_error_code__ = SO001

    @property
    def __validation_error_data__(self) -> ValidationErrorData:
        duplicate_periods_json: Json = {str(k): v for k, v in self.duplicate_periods.items()}
        series_code_or_id = SeriesCodeOrId(self.series_code, dataset_id=self.dataset_id)
        return ValidationErrorData(
            code=self.__validation_error_code__,
            extra={"duplicate_periods": duplicate_periods_json},
            path=series_code_or_id.validation_error_path,
        )


class InconsistentPeriodTypes(DataModelError):
    def __init__(
        self, *, dataset_id: "DatasetId | None" = None, period_types: set[type[Period]], series_code: "SeriesCode"
    ) -> None:
        series_code_or_id = SeriesCodeOrId(series_code, dataset_id=dataset_id)
        msg = f"Observation periods of the series {str(series_code_or_id)!r} have inconsistent types"
        super().__init__(msg=msg)
        self.dataset_id = dataset_id
        self.period_types = period_types
        self.series_code = series_code

    __validation_error_code__ = SO002

    @property
    def __validation_error_data__(self) -> ValidationErrorData:
        period_types_json = cast(Json, sorted(map(str, self.period_types)))
        series_code_or_id = SeriesCodeOrId(self.series_code, dataset_id=self.dataset_id)
        return ValidationErrorData(
            code=self.__validation_error_code__,
            extra={"period_types": period_types_json},
            path=series_code_or_id.validation_error_path,
        )


class UnorderedSeriesObservations(DataModelError):
    def __init__(
        self, *, dataset_id: "DatasetId | None" = None, first_diverging_index: int, series_code: "SeriesCode"
    ) -> None:
        series_code_or_id = SeriesCodeOrId(series_code, dataset_id=dataset_id)
        msg = f"Observation periods of the series {str(series_code_or_id)!r} are not sorted by period"
        super().__init__(msg=msg)
        self.dataset_id = dataset_id
        self.first_diverging_index = first_diverging_index
        self.series_code = series_code

    __validation_error_code__ = SO003

    @property
    def __validation_error_data__(self) -> ValidationErrorData:
        series_code_or_id = SeriesCodeOrId(self.series_code, dataset_id=self.dataset_id)
        return ValidationErrorData(
            code=self.__validation_error_code__,
            extra={"first_diverging_index": self.first_diverging_index},
            path=series_code_or_id.validation_error_path,
        )
