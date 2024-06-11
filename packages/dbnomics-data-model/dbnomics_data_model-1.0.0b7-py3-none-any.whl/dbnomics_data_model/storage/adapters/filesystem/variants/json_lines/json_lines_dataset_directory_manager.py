from collections.abc import Iterable, Iterator
from pathlib import Path

import daiquiri

from dbnomics_data_model.errors import DataModelError
from dbnomics_data_model.json_utils import save_jsonl_file
from dbnomics_data_model.json_utils.errors import JsonError
from dbnomics_data_model.model import DatasetId, DatasetMetadata, Series, SeriesCode
from dbnomics_data_model.model.identifiers.series_id import SeriesId
from dbnomics_data_model.model.revisions.types import RevisionId, RevisionMetadata
from dbnomics_data_model.storage.adapters.filesystem.base_dataset_directory_manager import BaseDatasetDirectoryManager
from dbnomics_data_model.storage.adapters.filesystem.constants import SERIES_JSONL
from dbnomics_data_model.storage.adapters.filesystem.errors.dataset_directory import DatasetDirectoryCreateError
from dbnomics_data_model.storage.adapters.filesystem.errors.dataset_json_file import (
    DatasetJsonDeleteError,
    DatasetJsonNotFound,
    DatasetJsonSaveError,
)
from dbnomics_data_model.storage.adapters.filesystem.git.git_provider_directory_manager import (
    GitProviderDirectoryManager,
)
from dbnomics_data_model.storage.adapters.filesystem.storage_variant import StorageVariant
from dbnomics_data_model.storage.adapters.filesystem.variants.json_lines.series_json_lines_item_repo import (
    SeriesJsonLinesItemRepo,
)
from dbnomics_data_model.storage.errors.dataset import (
    DatasetHasNoSeries,
    DatasetSeriesLoadError,
    DatasetSomeSeriesDeleteError,
    DatasetSomeSeriesLoadError,
    DatasetSomeSeriesNotFound,
    DatasetSomeSeriesSaveError,
)
from dbnomics_data_model.storage.errors.dataset_metadata import (
    DatasetMetadataDeleteError,
    DatasetMetadataNotFound,
    DatasetMetadataSaveError,
)
from dbnomics_data_model.storage.errors.revisions import LatestRevisionOnlyOperation, RevisionsNotAvailable

from .errors.series_json_lines_file import (
    SeriesJsonLinesDeleteError,
    SeriesJsonLinesFileError,
    SeriesJsonLinesNotFound,
    SeriesJsonLinesSaveError,
    SomeJsonLinesSeriesNotFound,
)
from .model.json_lines_dataset_json import JsonLinesDatasetJson
from .model.json_lines_series_item import JsonLinesSeriesItem
from .offsets.repo import JsonLinesSeriesOffsetRepo

__all__ = ["JsonLinesDatasetDirectoryManager"]

logger = daiquiri.getLogger(__name__)


class JsonLinesDatasetDirectoryManager(BaseDatasetDirectoryManager[JsonLinesDatasetJson]):
    def __init__(
        self,
        *,
        dataset_dir: Path | str,
        dataset_id: DatasetId,
        git_provider_directory_manager: GitProviderDirectoryManager | None = None,
        revision_id: RevisionId | None = None,
        series_offset_repo: JsonLinesSeriesOffsetRepo | None = None,
    ) -> None:
        super().__init__(
            dataset_dir=dataset_dir,
            dataset_id=dataset_id,
            git_provider_directory_manager=git_provider_directory_manager,
            revision_id=revision_id,
        )
        self._series_offset_repo = series_offset_repo

    def create_series_json_lines_items_repo(self) -> SeriesJsonLinesItemRepo:
        return SeriesJsonLinesItemRepo(
            dataset_id=self.dataset_id,
            git_provider_directory_manager=self._git_provider_directory_manager,
            revision_id=self.revision_id,
            series_jsonl_path=self.series_jsonl_path,
            series_offset_repo=self._series_offset_repo,
        )

    @property
    def dataset_json_class(self) -> type[JsonLinesDatasetJson]:
        return JsonLinesDatasetJson

    def delete_dataset_json(self, *, missing_ok: bool = False) -> None:
        if self.revision_id is not None:
            raise LatestRevisionOnlyOperation(revision_id=self.revision_id)

        dataset_json_path = self.dataset_json_path
        try:
            dataset_json_path.unlink(missing_ok=missing_ok)
        except FileNotFoundError as exc:
            raise DatasetJsonNotFound(dataset_id=self.dataset_id, dataset_json_path=dataset_json_path) from exc
        except Exception as exc:
            raise DatasetJsonDeleteError(dataset_id=self.dataset_id, dataset_json_path=dataset_json_path) from exc

    def delete_dataset_metadata(self, *, missing_ok: bool = False) -> None:
        if self.revision_id is not None:
            raise LatestRevisionOnlyOperation(revision_id=self.revision_id)

        try:
            self.delete_dataset_json(missing_ok=missing_ok)
        except DatasetJsonDeleteError as exc:
            raise DatasetMetadataDeleteError(dataset_id=self.dataset_id) from exc
        except DatasetJsonNotFound as exc:
            raise DatasetMetadataNotFound(dataset_id=self.dataset_id, revision_id=self.revision_id) from exc

    def delete_series(self, *, missing_ok: bool = False) -> None:
        if self.revision_id is not None:
            raise LatestRevisionOnlyOperation(revision_id=self.revision_id)

        try:
            self.delete_series_jsonl(missing_ok=missing_ok)
        except SeriesJsonLinesDeleteError as exc:
            raise DatasetSomeSeriesDeleteError(dataset_id=self.dataset_id) from exc
        except SeriesJsonLinesNotFound as exc:
            raise DatasetHasNoSeries(dataset_id=self.dataset_id) from exc

    def delete_series_jsonl(self, *, missing_ok: bool = False) -> None:
        if self.revision_id is not None:
            raise LatestRevisionOnlyOperation(revision_id=self.revision_id)

        series_jsonl_path = self.series_jsonl_path
        try:
            series_jsonl_path.unlink(missing_ok=missing_ok)
        except FileNotFoundError as exc:
            raise SeriesJsonLinesNotFound(dataset_id=self.dataset_id, series_jsonl_path=series_jsonl_path) from exc
        except Exception as exc:
            raise SeriesJsonLinesDeleteError(dataset_id=self.dataset_id, series_jsonl_path=series_jsonl_path) from exc

    def get_revision_metadata_for_series(self, series_code: SeriesCode) -> RevisionMetadata:
        metadata: RevisionMetadata = {"file": self.series_jsonl_path}

        if self._series_offset_repo is not None:
            series_id = SeriesId.from_dataset_id(self.dataset_id, series_code)
            offset = self._series_offset_repo.get_series_offset(series_id)
            if offset is not None:
                metadata["offset"] = offset

        return metadata

    def iter_json_lines_series_items(
        self, *, series_codes: list[SeriesCode] | None = None, with_observations: bool = True
    ) -> Iterator[JsonLinesSeriesItem]:
        series_json_lines_items_repo = self.create_series_json_lines_items_repo()
        try:
            yield from series_json_lines_items_repo.iter_json_lines_series_items(
                series_codes=series_codes, with_observations=with_observations
            )
        except (SeriesJsonLinesNotFound, SomeJsonLinesSeriesNotFound) as exc:
            raise DatasetSomeSeriesNotFound(dataset_id=self.dataset_id, revision_id=self.revision_id) from exc
        except SeriesJsonLinesFileError as exc:
            raise DatasetSomeSeriesLoadError(dataset_id=self.dataset_id, revision_id=self.revision_id) from exc

    def iter_series(
        self, *, series_codes: Iterable[SeriesCode] | None = None, with_observations: bool = True
    ) -> Iterator[Series]:
        try:
            dataset_metadata = self.load_dataset_metadata()
        except DatasetMetadataNotFound:
            dataset_dimensions = None
        else:
            dataset_dimensions = dataset_metadata.dimensions

        series_codes_list = None if series_codes is None else list(series_codes)

        for json_lines_series_item in self.iter_json_lines_series_items(
            series_codes=series_codes_list, with_observations=with_observations
        ):
            try:
                yield json_lines_series_item.to_domain_model(dataset_dimensions=dataset_dimensions)
            except DataModelError as exc:
                raise DatasetSeriesLoadError(
                    dataset_id=self.dataset_id,
                    revision_id=self.revision_id,
                    series_code=json_lines_series_item.code,
                ) from exc

    def matches_variant(self, *, revision_id: RevisionId | None = None) -> bool:
        series_jsonl_path = self.series_jsonl_path

        if revision_id is None:
            return series_jsonl_path.is_file()

        if self._git_provider_directory_manager is None:
            raise RevisionsNotAvailable

        return self._git_provider_directory_manager.has_file(series_jsonl_path, revision_id=revision_id)

    def save_dataset_metadata(self, dataset_metadata: DatasetMetadata) -> None:
        if self.revision_id is not None:
            raise LatestRevisionOnlyOperation(revision_id=self.revision_id)

        self._validate_dataset_metadata_code_matches(dataset_metadata)
        dataset_json = JsonLinesDatasetJson.from_domain_model(dataset_metadata)
        try:
            self.save_dataset_json(dataset_json)
        except (DatasetDirectoryCreateError, DatasetJsonSaveError) as exc:
            raise DatasetMetadataSaveError(dataset_id=self.dataset_id, dataset_metadata=dataset_metadata) from exc

    def save_series(self, series: Series | Iterable[Series]) -> None:
        if self.revision_id is not None:
            raise LatestRevisionOnlyOperation(revision_id=self.revision_id)

        # TODO track known series codes to ensure no duplicates are added
        series_iter = [series] if isinstance(series, Series) else series
        json_lines_series_items = (JsonLinesSeriesItem.from_domain_model(series) for series in series_iter)
        try:
            self.save_json_lines_series_items(json_lines_series_items)
        except SeriesJsonLinesSaveError as exc:
            raise DatasetSomeSeriesSaveError(dataset_id=self.dataset_id) from exc

    def save_json_lines_series_items(self, json_lines_series_items: Iterable[JsonLinesSeriesItem]) -> None:
        if self.revision_id is not None:
            raise LatestRevisionOnlyOperation(revision_id=self.revision_id)

        series_jsonl_path = self.series_jsonl_path

        series_json_data_iter = (
            json_lines_series_item.to_json_data() for json_lines_series_item in json_lines_series_items
        )

        try:
            save_jsonl_file(series_jsonl_path, series_json_data_iter, append_mode=True)
        except JsonError as exc:
            raise SeriesJsonLinesSaveError(dataset_id=self.dataset_id, series_jsonl_path=series_jsonl_path) from exc

    @property
    def series_jsonl_path(self) -> Path:
        return self.dataset_dir / SERIES_JSONL

    @property
    def storage_variant(self) -> StorageVariant:
        return StorageVariant.JSON_LINES
