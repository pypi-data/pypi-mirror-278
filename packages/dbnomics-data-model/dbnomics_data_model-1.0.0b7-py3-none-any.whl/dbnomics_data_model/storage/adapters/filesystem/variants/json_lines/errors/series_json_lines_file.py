from pathlib import Path

from dbnomics_data_model.json_utils import JsonObject
from dbnomics_data_model.model import DatasetId, SeriesCode, SeriesId
from dbnomics_data_model.model.revisions.types import RevisionId
from dbnomics_data_model.storage.adapters.filesystem.errors import FileSystemAdapterError


class SeriesJsonLinesFileError(FileSystemAdapterError):
    def __init__(self, *, dataset_id: DatasetId, msg: str, series_jsonl_path: Path) -> None:
        super().__init__(msg=msg)
        self.dataset_id = dataset_id
        self.series_jsonl_path = series_jsonl_path


class SeriesJsonDataParseError(SeriesJsonLinesFileError):
    def __init__(self, *, dataset_id: DatasetId, series_json_data: JsonObject, series_jsonl_path: Path) -> None:
        msg = f"Error parsing JSON data of a series of dataset {str(dataset_id)!r}"
        super().__init__(dataset_id=dataset_id, msg=msg, series_jsonl_path=series_jsonl_path)
        self.series_json_data = series_json_data


class SeriesJsonLinesDeleteError(SeriesJsonLinesFileError):
    def __init__(self, *, dataset_id: DatasetId, series_jsonl_path: Path) -> None:
        msg = f"Error deleting {series_jsonl_path} of dataset {str(dataset_id)!r}"
        super().__init__(msg=msg, dataset_id=dataset_id, series_jsonl_path=series_jsonl_path)


class SeriesJsonLinesNotFound(SeriesJsonLinesFileError):
    def __init__(self, *, dataset_id: DatasetId, series_jsonl_path: Path) -> None:
        msg = f"Could not find {series_jsonl_path} of dataset {str(dataset_id)!r}"
        super().__init__(msg=msg, dataset_id=dataset_id, series_jsonl_path=series_jsonl_path)


class SeriesJsonLinesSaveError(SeriesJsonLinesFileError):
    def __init__(self, *, dataset_id: DatasetId, series_jsonl_path: Path) -> None:
        msg = f"Error saving {series_jsonl_path} of dataset {str(dataset_id)!r}"
        super().__init__(msg=msg, dataset_id=dataset_id, series_jsonl_path=series_jsonl_path)


class SeriesJsonLinesScanError(SeriesJsonLinesFileError):
    def __init__(
        self, *, dataset_id: DatasetId, line_num: int, revision_id: RevisionId | None = None, series_jsonl_path: Path
    ) -> None:
        msg = f"Error loading one series of dataset {str(dataset_id)!r} from {series_jsonl_path} at line {line_num} at revision {revision_id!r}"
        super().__init__(dataset_id=dataset_id, msg=msg, series_jsonl_path=series_jsonl_path)
        self.line_num = line_num
        self.revision_id = revision_id


class SeriesJsonLineLoadError(SeriesJsonLinesFileError):
    """Base error for loading a particular line of series.jsonl."""

    def __init__(self, *, msg: str, offset: int, series_id: SeriesId, series_jsonl_path: Path) -> None:
        super().__init__(dataset_id=series_id.dataset_id, msg=msg, series_jsonl_path=series_jsonl_path)
        self.offset = offset
        self.series_code = series_id.series_code


class SeriesJsonLineCodeMismatch(SeriesJsonLineLoadError):
    def __init__(
        self, *, loaded_series_code: SeriesCode, offset: int, series_id: SeriesId, series_jsonl_path: Path
    ) -> None:
        msg = f"Expected series code {series_id.series_code!r} but got {loaded_series_code!r} from {series_jsonl_path} at {offset=}"  # noqa: E501
        super().__init__(msg=msg, offset=offset, series_id=series_id, series_jsonl_path=series_jsonl_path)
        self.loaded_series_code = loaded_series_code


class SeriesJsonLineParseError(SeriesJsonLineLoadError):
    def __init__(self, *, offset: int, series_id: SeriesId, series_jsonl_path: Path) -> None:
        msg = f"Error parsing series {str(series_id)!r} from JSON line of {series_jsonl_path} at {offset=}"
        super().__init__(msg=msg, offset=offset, series_id=series_id, series_jsonl_path=series_jsonl_path)


class SeriesJsonLineReadError(SeriesJsonLineLoadError):
    def __init__(self, *, offset: int, series_id: SeriesId, series_jsonl_path: Path) -> None:
        msg = f"Error reading JSON line of {series_jsonl_path} at {offset=} for series {str(series_id)!r}"
        super().__init__(msg=msg, offset=offset, series_id=series_id, series_jsonl_path=series_jsonl_path)


class SeriesJsonLineSeekError(SeriesJsonLineLoadError):
    def __init__(self, *, offset: int, series_id: SeriesId, series_jsonl_path: Path) -> None:
        msg = f"Error seeking file {series_jsonl_path} to {offset=} for series {str(series_id)!r}"
        super().__init__(msg=msg, offset=offset, series_id=series_id, series_jsonl_path=series_jsonl_path)


class SomeJsonLinesSeriesNotFound(SeriesJsonLinesFileError):
    def __init__(
        self,
        *,
        dataset_id: DatasetId,
        revision_id: RevisionId | None = None,
        series_codes: list[SeriesCode],
        series_jsonl_path: Path,
    ) -> None:
        msg = f"{len(series_codes)!r} series not found in {series_jsonl_path} of dataset {str(dataset_id)!r} at revision {revision_id!r}"  # noqa: E501
        super().__init__(dataset_id=dataset_id, msg=msg, series_jsonl_path=series_jsonl_path)
        self.revision_id = revision_id
        self.series_codes = series_codes
