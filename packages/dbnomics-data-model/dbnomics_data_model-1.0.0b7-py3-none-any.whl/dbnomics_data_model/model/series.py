from collections.abc import Iterator
from dataclasses import dataclass, field, replace
from datetime import date, datetime
from typing import Self

from more_itertools import minmax

from dbnomics_data_model.model.dimensions import dimension_utils
from dbnomics_data_model.model.dimensions.dataset_dimensions import DatasetDimensions
from dbnomics_data_model.model.errors.merge import MergeItemsMismatch
from dbnomics_data_model.model.observations.observation_value_range import ObservationValueRange
from dbnomics_data_model.model.observations.period_domain import PeriodDomain
from dbnomics_data_model.model.periods import Period
from dbnomics_data_model.model.url import PublicUrl
from dbnomics_data_model.utils import raise_first_error
from dbnomics_data_model.validation.series_dimension_validator import SeriesDimensionValidator
from dbnomics_data_model.validation.series_validator import SeriesValidator

from .errors.series import SeriesDimensionNotSet, SeriesHasNoDimension, SeriesHasNoObservation
from .identifiers.attribute_code import AttributeCode
from .identifiers.series_code import SeriesCode
from .identifiers.types import DimensionCode, DimensionValueCode
from .merge_utils import merge_iterables_of_items
from .observations import Observation, ObservationNumericValue, ObservationValue

__all__ = ["Series"]


@dataclass(kw_only=True)
class Series:
    # An attribute value can be a code or free text.
    attributes: dict[AttributeCode, str] = field(default_factory=dict)

    code: SeriesCode
    description: str | None = None
    dimensions: dict[DimensionCode, DimensionValueCode] = field(default_factory=dict)

    # URL to the documentation of the series.
    doc_href: PublicUrl | None = None

    name: str | None = None

    # When a new release of the series will occur, given by the provider.
    next_release_at: date | datetime | None = None

    notes: str | None = None
    observations: list[Observation] = field(default_factory=list)

    # When the series was last updated, given by the provider.
    updated_at: date | datetime | None = None

    def __post_init__(self) -> None:
        series_validator = SeriesValidator(series=self)
        raise_first_error(series_validator.iter_errors())

    @classmethod
    def create(
        cls,
        *,
        add_missing_dataset_dimensions: bool | set[DimensionCode] = False,
        attributes: dict[str, str] | None = None,
        code: str | None = None,
        dataset_dimensions: DatasetDimensions | None = None,
        description: str | None = None,
        dimensions: dict[str, str] | None = None,
        doc_href: str | None = None,
        name: str | None = None,
        next_release_at: date | datetime | None = None,
        notes: str | None = None,
        observations: list[Observation] | None = None,
        updated_at: date | datetime | None = None,
    ) -> Self:
        if attributes is None:
            attributes = {}
        parsed_attributes = cls._parse_attributes(attributes)

        if dimensions is None:
            dimensions = {}
        parsed_dimensions = cls._parse_dimensions(dimensions)

        if code is None:
            if dataset_dimensions is None:
                msg = "One of code or dataset_dimensions must be provided, but both are None"
                raise RuntimeError(msg)

            code = cls._generate_code_from_dimensions(parsed_dimensions, dataset_dimensions=dataset_dimensions)
        else:
            code = SeriesCode.parse(code)

        if doc_href is not None:
            doc_href = PublicUrl.parse(doc_href)

        if observations is None:
            observations = []

        if dataset_dimensions is None:
            if add_missing_dataset_dimensions:
                msg = "dataset_dimensions must not be None when using add_missing_dataset_dimensions"
                raise TypeError(msg)
        else:
            if add_missing_dataset_dimensions:
                dimension_utils.add_missing_dataset_dimensions(
                    dataset_dimensions, dimension_codes=add_missing_dataset_dimensions, dimensions=parsed_dimensions
                )

            series_dimension_validator = SeriesDimensionValidator(
                dataset_dimensions=dataset_dimensions, dimensions=parsed_dimensions, series_code=code
            )
            raise_first_error(series_dimension_validator.iter_errors())

        return cls(
            attributes=parsed_attributes,
            code=code,
            description=description,
            dimensions=parsed_dimensions,
            doc_href=doc_href,
            name=name,
            next_release_at=next_release_at,
            notes=notes,
            observations=observations,
            updated_at=updated_at,
        )

    def generate_name(self, dataset_dimensions: DatasetDimensions) -> str:
        """Generate a name for a time series based on its dimensions.

        It is impossible to generate a name without dimensions.
        """

        def iter_series_name_fragments() -> Iterator[str]:
            for dimension in dataset_dimensions:
                dimension_value_code = self.dimensions.get(dimension.code)
                if dimension_value_code is None:
                    raise SeriesDimensionNotSet(dimension=dimension, dimensions=self.dimensions, series=self)
                dimension_value = dimension.find_value_by_code(dimension_value_code)
                if dimension_value is None or dimension_value.label is None:
                    yield dimension_value_code
                else:
                    label_usage_count = len([v for v in dimension.values if v.label == dimension_value.label])
                    dimension_value_label = dimension_value.label
                    # If label is used more than once, add the code as a precision.
                    if label_usage_count > 1:
                        dimension_value_label += f" ({dimension_value_code})"
                    yield dimension_value_label

        if len(dataset_dimensions) == 0:
            raise SeriesHasNoDimension(series=self)

        return " - ".join(iter_series_name_fragments())

    def get_observation_attribute_codes(self) -> set[AttributeCode]:
        attribute_codes: set[AttributeCode] = set()
        for observation in self.observations:
            attribute_codes |= observation.attributes.keys()
        return attribute_codes

    def iter_periods(self) -> Iterator[Period]:
        return (observation.period for observation in self.observations)

    def iter_values(self) -> Iterator[ObservationValue]:
        return (observation.value for observation in self.observations)

    def merge(self, other: "Series") -> "Series":
        if self.code != other.code:
            raise MergeItemsMismatch(source=other, target=self)

        observations = merge_iterables_of_items(
            key=lambda observation: observation.period,
            merge=lambda _, target: target,
            sort_by_key=True,
            source=other.observations,
            target=self.observations,
        )

        return replace(
            other,
            # TODO add specific test to ensure that in case of conflict, the attributes of "other" are preferred
            attributes=self.attributes | other.attributes,
            # TODO add specific test to ensure that in case of conflict, the dimensions of "other" are preferred
            dimensions=self.dimensions | other.dimensions,
            observations=observations,
        )

    @property
    def max_period(self) -> Period:
        try:
            return max(self.iter_periods())
        except ValueError as exc:
            raise SeriesHasNoObservation(series=self) from exc

    @property
    def min_period(self) -> Period:
        try:
            return min(self.iter_periods())
        except ValueError as exc:
            raise SeriesHasNoObservation(series=self) from exc

    @property
    def max_value(self) -> ObservationNumericValue:
        try:
            return max(value for value in self.iter_values() if value is not None)
        except ValueError as exc:
            raise SeriesHasNoObservation(series=self) from exc

    @property
    def min_value(self) -> ObservationNumericValue:
        try:
            return min(value for value in self.iter_values() if value is not None)
        except ValueError as exc:
            raise SeriesHasNoObservation(series=self) from exc

    @property
    def period_domain(self) -> PeriodDomain | None:
        periods = list(self.iter_periods())
        if not periods:
            return None

        values = minmax(periods)
        return PeriodDomain(*values)

    @property
    def value_range(self) -> ObservationValueRange | None:
        numeric_values = [value for value in self.iter_values() if value is not None]
        if not numeric_values:
            return None

        values = minmax(numeric_values)
        return ObservationValueRange(*values)

    @classmethod
    def _generate_code_from_dimensions(
        cls, dimensions: dict[DimensionCode, DimensionValueCode], *, dataset_dimensions: DatasetDimensions
    ) -> SeriesCode:
        """Generate the code of a series from its dimensions, ordered as the dataset ones."""

        def iter_ordered_dimension_value_codes() -> Iterator[DimensionValueCode]:
            for dataset_dimension in dataset_dimensions:
                dimension_value_code = dimensions.get(dataset_dimension.code)
                if dimension_value_code is None:
                    raise SeriesDimensionNotSet(dimension=dataset_dimension, dimensions=dimensions, series=None)
                yield dimension_value_code

        return SeriesCode.parse(".".join(iter_ordered_dimension_value_codes()))

    @classmethod
    def _parse_attributes(cls, attributes: dict[str, str]) -> dict[AttributeCode, str]:
        return {AttributeCode.parse(code): value for code, value in attributes.items()}

    @classmethod
    def _parse_dimensions(cls, dimensions: dict[str, str]) -> dict[DimensionCode, DimensionValueCode]:
        return {
            DimensionCode.parse(code): DimensionValueCode.parse(value_code) for code, value_code in dimensions.items()
        }
