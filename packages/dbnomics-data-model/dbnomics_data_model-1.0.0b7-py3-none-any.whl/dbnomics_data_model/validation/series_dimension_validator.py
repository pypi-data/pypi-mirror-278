from collections.abc import Iterator

import daiquiri

from dbnomics_data_model.errors import DataModelError
from dbnomics_data_model.model.dimensions.dataset_dimensions import DatasetDimensions
from dbnomics_data_model.model.errors.frequency import InvalidFrequencyCode
from dbnomics_data_model.model.frequency import Frequency
from dbnomics_data_model.model.identifiers.dataset_id import DatasetId
from dbnomics_data_model.model.identifiers.series_code import SeriesCode
from dbnomics_data_model.model.identifiers.types import DimensionCode, DimensionValueCode
from dbnomics_data_model.validation.errors.series_dimension_validator import (
    SeriesInvalidFrequencyDimensionValue,
    SeriesUndefinedDimension,
    SeriesUndefinedDimensionValue,
)
from dbnomics_data_model.validation.validation_settings import current_validation_settings_var

logger = daiquiri.getLogger(__name__)


class SeriesDimensionValidator:
    def __init__(
        self,
        *,
        dataset_dimensions: DatasetDimensions,
        dataset_id: DatasetId | None = None,
        dimensions: dict[DimensionCode, DimensionValueCode],
        series_code: SeriesCode,
    ) -> None:
        self.dataset_dimensions = dataset_dimensions
        self.dataset_id = dataset_id
        self.dimensions = dimensions
        self.series_code = series_code

    def iter_errors(self) -> Iterator[DataModelError]:
        validation_settings = current_validation_settings_var.get()
        if not validation_settings.disable_series_validation:
            return

        yield from self._check_series_dimensions_exist()
        yield from self._validate_frequency_dimension()

    def _check_series_dimensions_exist(self) -> Iterator[DataModelError]:
        validation_settings = current_validation_settings_var.get()
        if not validation_settings.is_any_validation_code_enabled(
            SeriesUndefinedDimension.__validation_error_code__,
            SeriesUndefinedDimensionValue.__validation_error_code__,
        ):
            return

        dataset_dimensions = self.dataset_dimensions
        for dimension_code, dimension_value_code in self.dimensions.items():
            dimension = dataset_dimensions.find_dimension_by_code(dimension_code)
            if dimension is None:
                if validation_settings.is_validation_code_enabled(SeriesUndefinedDimension.__validation_error_code__):
                    yield SeriesUndefinedDimension(
                        dataset_dimensions=dataset_dimensions,
                        dataset_id=self.dataset_id,
                        dimension_code=dimension_code,
                        series_code=self.series_code,
                    )
                continue

            dimension_value = dimension.find_value_by_code(dimension_value_code)
            if dimension_value is None and validation_settings.is_validation_code_enabled(
                SeriesUndefinedDimensionValue.__validation_error_code__
            ):
                yield SeriesUndefinedDimensionValue(
                    dataset_id=self.dataset_id,
                    dimension=dimension,
                    dimension_value_code=dimension_value_code,
                    series_code=self.series_code,
                )

    def _validate_frequency_dimension(self) -> Iterator[DataModelError]:
        frequency_dimension_code = self.dataset_dimensions.frequency_dimension_code
        if frequency_dimension_code is None:
            return

        frequency_dimension_value_code = self.dimensions[frequency_dimension_code]

        try:
            Frequency.parse_code(frequency_dimension_value_code)
        except InvalidFrequencyCode as exc:
            error = SeriesInvalidFrequencyDimensionValue(
                dataset_id=self.dataset_id,
                dimension_code=frequency_dimension_code,
                dimension_value_code=frequency_dimension_value_code,
                series_code=self.series_code,
            )
            error.__cause__ = exc
            yield error
