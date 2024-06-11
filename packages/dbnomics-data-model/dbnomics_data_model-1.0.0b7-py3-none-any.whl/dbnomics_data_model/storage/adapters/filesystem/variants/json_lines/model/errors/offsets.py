from dbnomics_data_model.model.identifiers.series_id import SeriesId
from dbnomics_data_model.storage.adapters.filesystem.errors import FileSystemAdapterError


class JsonLinesSeriesOffsetRepoError(FileSystemAdapterError):
    pass


class SeriesMismatch(JsonLinesSeriesOffsetRepoError):
    def __init__(self, *, expected_series_id: SeriesId, found_series_id: SeriesId) -> None:
        msg = f"Series {str(expected_series_id)!r} was expected but {str(found_series_id)!r} was found"
        super().__init__(msg=msg)
        self.expected_series_id = expected_series_id
        self.found_series_id = found_series_id
