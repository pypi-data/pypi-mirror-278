from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import TypeVar

from dbnomics_data_model.model import Series
from dbnomics_data_model.model.dimensions.dataset_dimensions import DatasetDimensions
from dbnomics_data_model.storage.adapters.filesystem.model.base_json_model import BaseJsonObjectModel
from dbnomics_data_model.storage.adapters.filesystem.model.errors.base_series_json import (
    InconsistentDimensions,
    UnknownDimensionCodesOrder,
)

TBaseSeriesJson = TypeVar("TBaseSeriesJson", bound="BaseSeriesJson")


@dataclass(kw_only=True)
class BaseSeriesJson(BaseJsonObjectModel, ABC):
    """Base models for series metadata.

    Is subclassed to model JSON Lines and TSV variants.
    """

    code: str

    attributes: dict[str, str] = field(default_factory=dict)
    description: str | None = None

    # If it is a list, it must follow the same order than BaseDatasetJson.dimensions_codes_order.
    dimensions: dict[str, str] | list[str] = field(default_factory=dict[str, str])

    doc_href: str | None = None
    name: str | None = None
    next_release_at: date | datetime | None = None
    notes: str | None = None
    updated_at: date | datetime | None = None

    @classmethod
    @abstractmethod
    def from_domain_model(cls: type[TBaseSeriesJson], series: Series) -> TBaseSeriesJson: ...

    @abstractmethod
    def to_domain_model(self, *, dataset_dimensions: DatasetDimensions | None = None) -> Series: ...

    def _get_dimensions_as_dict(self, *, dataset_dimensions: DatasetDimensions | None) -> dict[str, str]:
        if isinstance(self.dimensions, dict):
            return self.dimensions

        assert isinstance(self.dimensions, list)

        if dataset_dimensions is None:
            raise UnknownDimensionCodesOrder(series_json=self)

        ordered_dimension_codes = dataset_dimensions.dimension_codes
        if len(ordered_dimension_codes) != len(self.dimensions):
            raise InconsistentDimensions(series_json=self)

        return dict(zip(ordered_dimension_codes, self.dimensions, strict=True))
