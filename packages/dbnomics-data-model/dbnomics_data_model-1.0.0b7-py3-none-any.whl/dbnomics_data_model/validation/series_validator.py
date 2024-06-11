from collections import Counter
from collections.abc import Iterator
from typing import TYPE_CHECKING

import daiquiri

from dbnomics_data_model.errors import DataModelError
from dbnomics_data_model.model.dimensions.dataset_dimensions import DatasetDimensions
from dbnomics_data_model.utils import find_index_of_first_difference
from dbnomics_data_model.validation.errors.series_validator import (
    DuplicateSeriesObservationPeriods,
    InconsistentPeriodTypes,
    UnorderedSeriesObservations,
)
from dbnomics_data_model.validation.series_dimension_validator import SeriesDimensionValidator
from dbnomics_data_model.validation.validation_settings import current_validation_settings_var

if TYPE_CHECKING:
    from dbnomics_data_model.model.identifiers.dataset_id import DatasetId
    from dbnomics_data_model.model.series import Series

logger = daiquiri.getLogger(__name__)


class SeriesValidator:
    def __init__(
        self,
        *,
        dataset_dimensions: DatasetDimensions | None = None,
        dataset_id: "DatasetId | None" = None,
        series: "Series",
    ) -> None:
        self.dataset_dimensions = dataset_dimensions
        self.dataset_id = dataset_id
        self.series = series

    def iter_errors(self) -> Iterator[DataModelError]:
        validation_settings = current_validation_settings_var.get()
        if not validation_settings.disable_series_validation:
            return

        yield from self._iter_dimension_errors()
        yield from self._iter_observation_errors()

    def _iter_dimension_errors(self) -> Iterator[DataModelError]:
        if self.dataset_dimensions is None:
            return

        series_dimension_validator = SeriesDimensionValidator(
            dataset_dimensions=self.dataset_dimensions,
            dataset_id=self.dataset_id,
            dimensions=self.series.dimensions,
            series_code=self.series.code,
        )
        yield from series_dimension_validator.iter_errors()

    def _iter_observation_errors(self) -> Iterator[DataModelError]:
        """Validate that the observation periods have a valid and homogeneous format, are unique and ordered."""
        observations = self.series.observations
        if not observations:
            return

        periods = [observation.period for observation in observations]
        duplicate_periods = {k: v for k, v in Counter(periods).items() if v > 1}
        if duplicate_periods:
            yield DuplicateSeriesObservationPeriods(
                dataset_id=self.dataset_id, duplicate_periods=duplicate_periods, series_code=self.series.code
            )

        periods_sorted = sorted(set(periods))
        first_diverging_index = find_index_of_first_difference(periods, periods_sorted)
        if first_diverging_index is not None:
            yield UnorderedSeriesObservations(
                dataset_id=self.dataset_id, first_diverging_index=first_diverging_index, series_code=self.series.code
            )

        period_types = {type(period) for period in periods}
        if len(period_types) > 1:
            yield InconsistentPeriodTypes(
                dataset_id=self.dataset_id, period_types=period_types, series_code=self.series.code
            )
