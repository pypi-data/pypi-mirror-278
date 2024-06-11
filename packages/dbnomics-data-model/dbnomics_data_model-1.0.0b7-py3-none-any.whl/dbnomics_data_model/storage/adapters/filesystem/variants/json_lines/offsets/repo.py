from abc import ABC, abstractmethod
from collections.abc import Iterable, Iterator

from dbnomics_data_model.model import SeriesId
from dbnomics_data_model.storage.adapters.filesystem.variants.json_lines.model.errors.offsets import SeriesMismatch
from dbnomics_data_model.storage.adapters.filesystem.variants.json_lines.offsets.types import JsonLinesOffset


class JsonLinesSeriesOffsetRepo(ABC):
    def get_series_offset(self, series_id: SeriesId) -> JsonLinesOffset | None:
        try:
            found_series_id, offset = next(self.iter_series_offsets([series_id]))
        except StopIteration:
            return None

        if series_id != found_series_id:
            raise SeriesMismatch(expected_series_id=series_id, found_series_id=found_series_id)

        return offset

    @abstractmethod
    def iter_series_offsets(self, series_ids: Iterable[SeriesId]) -> Iterator[tuple[SeriesId, JsonLinesOffset]]: ...
