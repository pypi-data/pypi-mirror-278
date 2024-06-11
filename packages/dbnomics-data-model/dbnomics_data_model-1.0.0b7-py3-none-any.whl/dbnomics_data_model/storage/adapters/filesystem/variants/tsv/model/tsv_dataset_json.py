from dataclasses import dataclass, field

from dbnomics_data_model.model import Series
from dbnomics_data_model.storage.adapters.filesystem.model.base_dataset_json import BaseDatasetJson
from dbnomics_data_model.utils import find_index

from .tsv_series_json import TsvSeriesJson

__all__ = ["TsvDatasetJson"]


@dataclass(kw_only=True)
class TsvDatasetJson(BaseDatasetJson):
    """Model for dataset.json following the TSV storage variant.

    Contains dataset metadata and series metadata.
    """

    series: list[TsvSeriesJson] = field(default_factory=list)

    def update_series_metadata(self, series: Series) -> None:
        """Add series metadata if it does not exist, otherwise replace it."""
        existing_series_index = find_index(lambda series: series.code == series.code, self.series)
        series_json = TsvSeriesJson.from_domain_model(series)
        if existing_series_index is None:
            self.series.append(series_json)
        else:
            self.series[existing_series_index] = series_json
