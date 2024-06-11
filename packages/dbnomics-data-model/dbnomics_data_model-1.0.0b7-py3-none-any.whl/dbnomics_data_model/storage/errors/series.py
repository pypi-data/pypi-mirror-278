from dbnomics_data_model.errors import DataModelError
from dbnomics_data_model.model import SeriesId
from dbnomics_data_model.model.revisions.types import RevisionId


class SeriesStorageError(DataModelError):
    def __init__(self, *, msg: str, series_id: SeriesId) -> None:
        super().__init__(msg=msg)
        self.series_id = series_id


class SeriesLoadError(SeriesStorageError):
    def __init__(self, *, revision_id: RevisionId | None = None, series_id: SeriesId) -> None:
        msg = f"Error loading series {str(series_id)!r} at revision {revision_id!r}"
        super().__init__(msg=msg, series_id=series_id)
        self.revision_id = revision_id


class SeriesNotFound(SeriesStorageError):
    def __init__(self, *, revision_id: RevisionId | None = None, series_id: SeriesId) -> None:
        msg = f"Could not find series {str(series_id)!r} at revision {revision_id!r}"
        super().__init__(msg=msg, series_id=series_id)
        self.revision_id = revision_id
