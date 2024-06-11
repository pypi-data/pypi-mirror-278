from collections.abc import Iterable, Iterator
from typing import TYPE_CHECKING

from dbnomics_data_model.model import SeriesId
from dbnomics_data_model.storage.adapters.filesystem.variants.json_lines.offsets.repo import JsonLinesSeriesOffsetRepo
from dbnomics_data_model.storage.adapters.filesystem.variants.json_lines.offsets.types import JsonLinesOffset

if TYPE_CHECKING:
    from dbnomics_data_model.dbnomics_solr_client import DBnomicsSolrClient


class SolrJsonLinesSeriesOffsetRepo(JsonLinesSeriesOffsetRepo):
    def __init__(self, *, dbnomics_solr_client: "DBnomicsSolrClient") -> None:
        super().__init__()
        self._dbnomics_solr_client = dbnomics_solr_client

    def iter_series_offsets(self, series_ids: Iterable[SeriesId]) -> Iterator[tuple[SeriesId, JsonLinesOffset]]:
        for series_id in series_ids:
            series_solr_doc = self._dbnomics_solr_client.find_series(series_id)
            if series_solr_doc is None:
                continue
            offset = series_solr_doc.series_jsonl_offset
            if offset is None:
                continue
            yield series_id, offset
