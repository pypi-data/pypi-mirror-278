from typing import Self, cast

from dbnomics_data_model.model import Series
from dbnomics_data_model.model.dimensions.dataset_dimensions import DatasetDimensions
from dbnomics_data_model.storage.adapters.filesystem.model.base_series_json import BaseSeriesJson

__all__ = ["TsvSeriesJson"]


class TsvSeriesJson(BaseSeriesJson):
    """An item of series metadata in dataset.json following the TSV storage variant."""

    @classmethod
    def from_domain_model(cls, series: Series) -> Self:
        attributes = cast(dict[str, str], series.attributes)
        dimensions = cast(dict[str, str], series.dimensions)
        return cls(
            attributes=attributes,
            code=series.code,
            description=series.description,
            dimensions=dimensions,
            doc_href=series.doc_href,
            name=series.name,
            next_release_at=series.next_release_at,
            notes=series.notes,
            updated_at=series.updated_at,
        )

    def to_domain_model(self, *, dataset_dimensions: DatasetDimensions | None = None) -> Series:
        dimensions = self._get_dimensions_as_dict(dataset_dimensions=dataset_dimensions)
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
            updated_at=self.updated_at,
        )
