from pathlib import Path

from dbnomics_data_model.model import DatasetId, SeriesCode
from dbnomics_data_model.model.revisions.types import RevisionId
from dbnomics_data_model.storage.adapters.filesystem.errors import FileSystemAdapterError


class SeriesTsvFileError(FileSystemAdapterError):
    def __init__(self, *, dataset_id: DatasetId, msg: str, series_tsv_path: Path) -> None:
        super().__init__(msg=msg)
        self.dataset_id = dataset_id
        self.series_tsv_path = series_tsv_path


class SeriesTsvDeleteError(SeriesTsvFileError):
    def __init__(self, *, dataset_id: DatasetId, series_tsv_path: Path) -> None:
        msg = f"Error deleting series TSV file {series_tsv_path}"
        super().__init__(dataset_id=dataset_id, msg=msg, series_tsv_path=series_tsv_path)


class SeriesTsvLoadError(SeriesTsvFileError):
    def __init__(
        self,
        *,
        dataset_id: DatasetId,
        revision_id: RevisionId | None = None,
        series_code: SeriesCode,
        series_tsv_path: Path,
    ) -> None:
        msg = f"Error loading series {series_code!r} from TSV file {series_tsv_path} at revision {revision_id!r}"
        super().__init__(dataset_id=dataset_id, msg=msg, series_tsv_path=series_tsv_path)
        self.revision_id = revision_id
        self.series_code = series_code


class SeriesTsvNotFound(SeriesTsvFileError):
    def __init__(self, *, dataset_id: DatasetId, series_code: SeriesCode, series_tsv_path: Path) -> None:
        msg = f"Could not find {series_tsv_path} of series {series_code!r}"
        super().__init__(dataset_id=dataset_id, msg=msg, series_tsv_path=series_tsv_path)
        self.series_code = series_code


class SeriesTsvSaveError(SeriesTsvFileError):
    def __init__(self, *, dataset_id: DatasetId, series_code: SeriesCode, series_tsv_path: Path) -> None:
        msg = f"Error saving series {series_code!r} to TSV file {series_tsv_path}"
        super().__init__(dataset_id=dataset_id, msg=msg, series_tsv_path=series_tsv_path)
        self.series_code = series_code
