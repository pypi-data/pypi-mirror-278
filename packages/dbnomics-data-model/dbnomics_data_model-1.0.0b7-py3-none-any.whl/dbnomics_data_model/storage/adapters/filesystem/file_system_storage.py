import shutil
from collections.abc import Iterable, Iterator
from pathlib import Path
from typing import TYPE_CHECKING

import daiquiri

from dbnomics_data_model.diff_utils.data_patch import DataPatch
from dbnomics_data_model.model import (
    CategoryTree,
    DatasetCode,
    DatasetId,
    DatasetMetadata,
    DatasetReleases,
    ProviderCode,
    ProviderMetadata,
    Series,
    SeriesCode,
    SeriesId,
)
from dbnomics_data_model.model.revisions.revision import Revision
from dbnomics_data_model.model.revisions.types import RevisionId
from dbnomics_data_model.storage.adapters.filesystem.constants import PROVIDER_JSON
from dbnomics_data_model.storage.adapters.filesystem.errors.dataset_directory import (
    DatasetDirectoryError,
    DatasetDirectoryNotFound,
)
from dbnomics_data_model.storage.adapters.filesystem.errors.dataset_json_file import DatasetJsonDeleteError
from dbnomics_data_model.storage.adapters.filesystem.errors.file_system_storage import StorageDirectoryNotFound
from dbnomics_data_model.storage.adapters.filesystem.errors.provider_directory import (
    ProviderDirectoryDeleteError,
    ProviderDirectoryNotFound,
)
from dbnomics_data_model.storage.adapters.filesystem.errors.releases_json_file import ReleasesJsonDeleteError
from dbnomics_data_model.storage.adapters.filesystem.file_system_storage_session import FileSystemStorageSession
from dbnomics_data_model.storage.errors.dataset import DatasetDeleteError, DatasetNotFound
from dbnomics_data_model.storage.errors.dataset_metadata import DatasetMetadataDeleteError
from dbnomics_data_model.storage.errors.dataset_releases import DatasetReleasesDeleteError
from dbnomics_data_model.storage.errors.provider import ProviderDeleteError, ProviderNotFound
from dbnomics_data_model.storage.errors.provider_metadata import ProviderMetadataLoadError
from dbnomics_data_model.storage.storage import Storage

from .file_utils import iter_child_directories
from .provider_directory_manager import ProviderDirectoryManager, create_provider_directory_manager
from .storage_variant import StorageVariant
from .variants.json_lines.offsets.repo import JsonLinesSeriesOffsetRepo

if TYPE_CHECKING:
    from dbnomics_data_model.storage.adapters.filesystem.file_system_storage_uri import FileSystemStorageUri


__all__ = ["FileSystemStorage"]


logger = daiquiri.getLogger(__name__)


class FileSystemStorage(Storage):
    """File-system concrete implementation of Storage.

    Series can be stored in the file-system with 2 variants:
    - TSV: series metadata is in `dataset.json` under the `series` array property,
        and observations are in TSV files
    - JSON lines: series metadata and observations are in `series.jsonl`
    """

    def __init__(
        self,
        *,
        auto_create: bool = True,
        storage_dir: Path,
        default_storage_variant: StorageVariant | None = None,
        series_offset_repo: JsonLinesSeriesOffsetRepo | None = None,
    ) -> None:
        self.auto_create = auto_create

        if not storage_dir.is_dir():
            if auto_create:
                storage_dir.mkdir()
            else:
                raise StorageDirectoryNotFound(storage_dir=storage_dir)
        self.storage_dir = storage_dir

        if default_storage_variant is None:
            default_storage_variant = StorageVariant.JSON_LINES
        self.default_storage_variant = default_storage_variant

        self._series_offset_repo = series_offset_repo

    @classmethod
    def from_uri(cls, uri: "FileSystemStorageUri") -> "FileSystemStorage":  # type: ignore[override]
        storage_dir = uri.path

        if uri.params.single_provider:
            from dbnomics_data_model.storage.adapters.filesystem.single_provider_file_system_storage import (
                SingleProviderFileSystemStorage,
            )

            return SingleProviderFileSystemStorage(
                auto_create=uri.params.auto_create,
                storage_dir=storage_dir,
                default_storage_variant=uri.params.variant,
                series_offset_repo=uri.params.series_offset_repo,
            )

        return FileSystemStorage(
            auto_create=uri.params.auto_create,
            storage_dir=storage_dir,
            default_storage_variant=uri.params.variant,
            series_offset_repo=uri.params.series_offset_repo,
        )

    def clone(self, *, storage_dir: Path) -> "FileSystemStorage":
        return FileSystemStorage(
            auto_create=self.auto_create,
            default_storage_variant=self.default_storage_variant,
            series_offset_repo=self._series_offset_repo,
            storage_dir=storage_dir,
        )

    def create_provider_directory_manager(
        self, provider_code: ProviderCode, *, ensure_dir: bool = False
    ) -> ProviderDirectoryManager:
        provider_dir = self.get_provider_dir(provider_code)
        if ensure_dir:
            provider_dir.mkdir(exist_ok=True)

        try:
            return create_provider_directory_manager(
                provider_code=provider_code,
                provider_dir=provider_dir,
                default_storage_variant=self.default_storage_variant,
                series_offset_repo=self._series_offset_repo,
            )
        except ProviderDirectoryNotFound as exc:
            raise ProviderNotFound(provider_code=provider_code) from exc

    def create_session(self, name: str) -> FileSystemStorageSession:
        return FileSystemStorageSession.from_storage(self, session_name=name)

    def delete_category_tree(self, provider_code: ProviderCode, *, missing_ok: bool = False) -> None:
        provider_directory_manager = self.create_provider_directory_manager(provider_code)
        provider_directory_manager.delete_category_tree(missing_ok=missing_ok)

    def delete_dataset(self, dataset_id: DatasetId, *, missing_ok: bool = False) -> None:
        provider_directory_manager = self.create_provider_directory_manager(dataset_id.provider_code)
        try:
            provider_directory_manager.delete_dataset(dataset_id.dataset_code, missing_ok=missing_ok)
        except DatasetDirectoryNotFound as exc:
            raise DatasetNotFound(dataset_id=dataset_id) from exc
        except DatasetDirectoryError as exc:
            raise DatasetDeleteError(dataset_id=dataset_id) from exc

    def delete_dataset_metadata(self, dataset_id: DatasetId, *, missing_ok: bool = False) -> None:
        provider_directory_manager = self.create_provider_directory_manager(dataset_id.provider_code)
        try:
            return provider_directory_manager.delete_dataset_metadata(dataset_id.dataset_code, missing_ok=missing_ok)
        except DatasetJsonDeleteError as exc:
            raise DatasetMetadataDeleteError(dataset_id=dataset_id) from exc

    def delete_dataset_releases(self, provider_code: ProviderCode, *, missing_ok: bool = False) -> None:
        provider_directory_manager = self.create_provider_directory_manager(provider_code)
        try:
            provider_directory_manager.delete_dataset_releases(missing_ok=missing_ok)
        except ReleasesJsonDeleteError as exc:
            raise DatasetReleasesDeleteError(provider_code=provider_code) from exc

    def delete_dataset_series(self, dataset_id: DatasetId, *, missing_ok: bool = False) -> None:
        provider_directory_manager = self.create_provider_directory_manager(dataset_id.provider_code)
        provider_directory_manager.delete_dataset_series(dataset_id.dataset_code, missing_ok=missing_ok)

    def delete_provider(self, provider_code: ProviderCode, *, missing_ok: bool = False) -> None:
        try:
            self.delete_provider_dir(provider_code, missing_ok=missing_ok)
        except ProviderDirectoryDeleteError as exc:
            raise ProviderDeleteError(provider_code=provider_code) from exc
        except ProviderDirectoryNotFound as exc:
            raise ProviderNotFound(provider_code=provider_code) from exc

    def delete_provider_dir(self, provider_code: ProviderCode, *, missing_ok: bool = False) -> None:
        provider_dir = self.get_provider_dir(provider_code)

        if not provider_dir.is_dir():
            if not missing_ok:
                raise ProviderDirectoryNotFound(provider_code=provider_code, provider_dir=provider_dir)
            return

        try:
            shutil.rmtree(provider_dir)
        except Exception as exc:
            raise ProviderDirectoryDeleteError(provider_code=provider_code, provider_dir=provider_dir) from exc

    def delete_provider_metadata(self, provider_code: ProviderCode, *, missing_ok: bool = False) -> None:
        provider_directory_manager = self.create_provider_directory_manager(provider_code)
        provider_directory_manager.delete_provider_metadata(missing_ok=missing_ok)

    def get_provider_dir(self, provider_code: ProviderCode) -> Path:
        return self.storage_dir / self.get_provider_dir_name(provider_code)

    def get_provider_dir_name(self, provider_code: ProviderCode) -> str:
        return f"{provider_code.lower()}-json-data"

    def has_dataset(self, dataset_id: DatasetId, *, revision_id: RevisionId | None = None) -> bool:
        try:
            provider_directory_manager = self.create_provider_directory_manager(dataset_id.provider_code)
        except ProviderNotFound:
            return False
        return provider_directory_manager.has_dataset(dataset_id.dataset_code, revision_id=revision_id)

    def has_dataset_metadata(self, dataset_id: DatasetId, *, revision_id: RevisionId | None = None) -> bool:
        provider_directory_manager = self.create_provider_directory_manager(dataset_id.provider_code)
        return provider_directory_manager.has_dataset_metadata(dataset_id.dataset_code, revision_id=revision_id)

    def has_series(self, series_id: SeriesId, *, revision_id: RevisionId | None = None) -> bool:
        provider_directory_manager = self.create_provider_directory_manager(series_id.provider_code)
        return provider_directory_manager.has_series(
            series_id.series_code, dataset_code=series_id.dataset_code, revision_id=revision_id
        )

    def iter_dataset_codes(
        self, provider_code: ProviderCode, *, revision_id: RevisionId | None = None
    ) -> Iterator[DatasetCode]:
        provider_directory_manager = self.create_provider_directory_manager(provider_code)
        yield from provider_directory_manager.iter_dataset_codes(revision_id=revision_id)

    def iter_dataset_releases(
        self, provider_code: ProviderCode, *, revision_id: RevisionId | None = None
    ) -> Iterator[DatasetReleases]:
        provider_directory_manager = self.create_provider_directory_manager(provider_code)
        yield from provider_directory_manager.iter_dataset_releases(revision_id=revision_id)

    def iter_dataset_series(
        self,
        dataset_id: DatasetId,
        *,
        revision_id: RevisionId | None = None,
        series_codes: Iterable[SeriesCode] | None = None,
        with_observations: bool = True,
    ) -> Iterator[Series]:
        provider_directory_manager = self.create_provider_directory_manager(dataset_id.provider_code)
        yield from provider_directory_manager.iter_dataset_series(
            dataset_id.dataset_code,
            revision_id=revision_id,
            series_codes=series_codes,
            with_observations=with_observations,
        )

    def iter_provider_codes(self, *, revision_id: RevisionId | None = None) -> Iterator[ProviderCode]:
        for provider_dir in self.iter_provider_directories():
            provider_directory_manager = ProviderDirectoryManager.open(
                provider_dir=provider_dir,
                default_storage_variant=self.default_storage_variant,
                series_offset_repo=self._series_offset_repo,
            )

            try:
                provider_metadata = provider_directory_manager.load_provider_metadata(revision_id=revision_id)
            except ProviderMetadataLoadError:
                logger.exception(
                    "The child directory %s was not recognized as containing provider data, ignoring", str(provider_dir)
                )
                continue

            yield provider_metadata.code

    def iter_provider_directories(self) -> Iterator[Path]:
        yield from self._iter_child_directories(ignore_hidden=True)

    def iter_series_changes(
        self,
        series_id: SeriesId,
        *,
        start_revision_id: RevisionId | None = None,
    ) -> Iterator[tuple[Revision, DataPatch]]:
        provider_directory_manager = self.create_provider_directory_manager(series_id.provider_code)
        return provider_directory_manager.iter_series_changes(
            series_id.series_code,
            dataset_code=series_id.dataset_code,
            start_revision_id=start_revision_id,
        )

    def load_category_tree(
        self, provider_code: ProviderCode, *, revision_id: RevisionId | None = None
    ) -> CategoryTree | None:
        provider_directory_manager = self.create_provider_directory_manager(provider_code)
        return provider_directory_manager.load_category_tree(revision_id=revision_id)

    def load_dataset_metadata(self, dataset_id: DatasetId, *, revision_id: RevisionId | None = None) -> DatasetMetadata:
        provider_directory_manager = self.create_provider_directory_manager(dataset_id.provider_code)
        return provider_directory_manager.load_dataset_metadata(dataset_id.dataset_code, revision_id=revision_id)

    def load_provider_metadata(
        self, provider_code: ProviderCode, *, revision_id: RevisionId | None = None
    ) -> ProviderMetadata:
        provider_directory_manager = self.create_provider_directory_manager(provider_code)
        return provider_directory_manager.load_provider_metadata(revision_id=revision_id)

    def load_series(
        self,
        series_id: SeriesId,
        *,
        revision_id: RevisionId | None = None,
        with_observations: bool = True,
    ) -> Series:
        provider_directory_manager = self.create_provider_directory_manager(series_id.provider_code)
        return provider_directory_manager.load_series(
            series_id.series_code,
            dataset_code=series_id.dataset_code,
            revision_id=revision_id,
            with_observations=with_observations,
        )

    def save_category_tree(self, category_tree: CategoryTree, *, provider_code: ProviderCode) -> None:
        provider_directory_manager = self.create_provider_directory_manager(provider_code, ensure_dir=True)
        provider_directory_manager.save_category_tree(category_tree)

    def save_dataset_metadata(self, dataset_metadata: DatasetMetadata, *, provider_code: ProviderCode) -> None:
        provider_directory_manager = self.create_provider_directory_manager(provider_code, ensure_dir=True)
        provider_directory_manager.save_dataset_metadata(dataset_metadata)

    def save_dataset_releases(
        self, dataset_releases: DatasetReleases | Iterable[DatasetReleases], *, provider_code: ProviderCode
    ) -> None:
        provider_directory_manager = self.create_provider_directory_manager(provider_code, ensure_dir=True)
        provider_directory_manager.save_dataset_releases(dataset_releases)

    def save_provider_metadata(self, provider_metadata: ProviderMetadata) -> None:
        provider_code = provider_metadata.code
        provider_directory_manager = self.create_provider_directory_manager(provider_code, ensure_dir=True)
        provider_directory_manager.save_provider_metadata(provider_metadata)

    def save_series(self, series: Series | Iterable[Series], *, dataset_id: DatasetId) -> None:
        provider_directory_manager = self.create_provider_directory_manager(dataset_id.provider_code, ensure_dir=True)
        provider_directory_manager.save_series(series, dataset_code=dataset_id.dataset_code)

    def _iter_child_directories(self, *, ignore_hidden: bool = False) -> Iterator[Path]:
        for child_dir in iter_child_directories(self.storage_dir, ignore_hidden=ignore_hidden):
            if not (child_dir / PROVIDER_JSON).is_file():
                logger.debug("Ignoring directory without a %r file", PROVIDER_JSON, child_dir=child_dir)
                continue

            yield child_dir
