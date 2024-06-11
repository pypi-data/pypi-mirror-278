from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import Self, TypeAlias, cast

from dbnomics_data_model.model import Observation, ObservationValue, Series
from dbnomics_data_model.model.constants import PERIOD, VALUE
from dbnomics_data_model.model.dimensions.dataset_dimensions import DatasetDimensions
from dbnomics_data_model.storage.adapters.filesystem.constants import NOT_AVAILABLE
from dbnomics_data_model.storage.adapters.filesystem.model.base_series_json import BaseSeriesJson

from .errors.json_lines_series_item import (
    InvalidObservationValue,
    ObservationAttributeCodeTypeError,
    ObservationPeriodTypeError,
)

__all__ = ["JsonLinesSeriesItem"]


ObservationJson: TypeAlias = list[float | str | None]


@dataclass(kw_only=True)
class JsonLinesSeriesItem(BaseSeriesJson):
    """A line of series.jsonl representing a single series following the JSON Lines storage variant.

    Contains series metadata and observations.
    """

    # Can't express heterogeneous variadic tuple type like (str, float | str, str...),
    # so declaring a simple type here and continuing parsing in self._iter_observations().
    observations: list[ObservationJson] = field(default_factory=list)

    @classmethod
    def from_domain_model(cls, series: Series) -> Self:
        attributes = cast(dict[str, str], series.attributes)
        dimensions = cast(dict[str, str], series.dimensions)
        observations = list(cls._iter_observations_json(series))
        return cls(
            attributes=attributes,
            code=series.code,
            description=series.description,
            dimensions=dimensions,
            doc_href=series.doc_href,
            name=series.name,
            next_release_at=series.next_release_at,
            notes=series.notes,
            observations=observations,
            updated_at=series.updated_at,
        )

    def to_domain_model(self, *, dataset_dimensions: DatasetDimensions | None = None) -> Series:
        dimensions = self._get_dimensions_as_dict(dataset_dimensions=dataset_dimensions)
        observations = list(self._iter_observations_as_domain_model())
        return Series.create(
            attributes=self.attributes,
            code=self.code,
            dataset_dimensions=dataset_dimensions,
            description=self.description,
            dimensions=dimensions,
            doc_href=self.doc_href,
            name=self.name,
            next_release_at=self.next_release_at,
            notes=self.notes,
            observations=observations,
            updated_at=self.updated_at,
        )

    def _iter_observations_as_domain_model(self) -> Iterator[Observation]:
        observations_json = self.observations

        if len(observations_json) < 2:  # noqa: PLR2004
            return

        header_json = observations_json[0]
        all_attribute_codes = self._parse_attribute_codes(header_json)

        for observation_json in observations_json[1:]:
            attributes = self._parse_attributes(observation_json, all_attribute_codes=all_attribute_codes)
            period = self._parse_period(observation_json)
            value = self._parse_value(observation_json)
            yield Observation.create(attributes=attributes, period=period, value=value)

    @classmethod
    def _iter_observations_json(cls, series: Series) -> Iterator[ObservationJson]:
        all_attribute_codes = sorted(series.get_observation_attribute_codes())

        yield [PERIOD, VALUE, *all_attribute_codes]

        for observation in series.observations:
            value_json = NOT_AVAILABLE if observation.value is None else float(observation.value)
            attributes = [observation.attributes.get(code, "") for code in all_attribute_codes]
            yield [str(observation.period), cast(float | str, value_json), *attributes]

    def _parse_attribute_codes(self, header_json: ObservationJson) -> list[str]:
        attribute_codes_json = cast(list[str | None], header_json[2:])
        if not all(isinstance(code, str) for code in attribute_codes_json):
            raise ObservationAttributeCodeTypeError(
                json_lines_series_item=self, attribute_codes_json=attribute_codes_json
            )

        return cast(list[str], attribute_codes_json)

    def _parse_attributes(self, observation_json: ObservationJson, *, all_attribute_codes: list[str]) -> dict[str, str]:
        attribute_value_codes_json = cast(list[str | None], observation_json[2:])
        if not all(isinstance(code, str | None) for code in attribute_value_codes_json):
            raise ObservationAttributeCodeTypeError(
                json_lines_series_item=self, attribute_codes_json=attribute_value_codes_json
            )

        return {
            attribute_code: attribute_value_code
            for attribute_code, attribute_value_code in zip(
                all_attribute_codes, attribute_value_codes_json, strict=True
            )
            if attribute_value_code is not None
        }

    def _parse_period(self, observation_json: ObservationJson) -> str:
        period_json = observation_json[0]
        if not isinstance(period_json, str):
            raise ObservationPeriodTypeError(json_lines_series_item=self, period_json=period_json)

        return period_json

    def _parse_value(self, observation_json: ObservationJson) -> ObservationValue:
        value_json = observation_json[1]
        if value_json == NOT_AVAILABLE or value_json is None:
            return None
        if isinstance(value_json, float):
            return value_json

        raise InvalidObservationValue(json_lines_series_item=self, value_json=value_json)
