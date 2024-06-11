import contextlib
import shutil
from collections.abc import Iterable, Iterator
from dataclasses import replace
from functools import lru_cache
from pathlib import Path

import daiquiri
from jsonalias import Json

from dbnomics_data_model.diff_utils.data_differ import DataDiffer
from dbnomics_data_model.diff_utils.data_patch import DataPatch
from dbnomics_data_model.errors import DataModelError
from dbnomics_data_model.file_utils import format_file_path_with_size
from dbnomics_data_model.json_utils import save_json_file
from dbnomics_data_model.json_utils.errors import JsonError, JsonParseError
from dbnomics_data_model.json_utils.parsing import parse_json_file
from dbnomics_data_model.model import (
    CategoryTree,
    DatasetCode,
    DatasetMetadata,
    DatasetReleases,
    ProviderCode,
    ProviderMetadata,
    Series,
    SeriesCode,
)
from dbnomics_data_model.model.errors.provider_metadata import ProviderMetadataCodeMismatch
from dbnomics_data_model.model.identifiers import DatasetId
from dbnomics_data_model.model.identifiers.errors import DatasetCodeParseError
from dbnomics_data_model.model.identifiers.series_id import SeriesId
from dbnomics_data_model.model.revisions.revision import Revision
from dbnomics_data_model.model.revisions.types import RevisionId
from dbnomics_data_model.revision_utils import iter_revision_pairs
from dbnomics_data_model.storage.adapters.filesystem.base_dataset_directory_manager import (
    create_dataset_directory_manager,
)
from dbnomics_data_model.storage.adapters.filesystem.errors.git_provider_directory_manager import (
    BlobNotFound,
    GitProviderDirectoryManagerError,
)
from dbnomics_data_model.storage.adapters.filesystem.errors.json_model import JsonModelError
from dbnomics_data_model.storage.adapters.filesystem.errors.provider_directory_manager import ProviderJsonCodeMismatch
from dbnomics_data_model.storage.adapters.filesystem.errors.releases_json_file import (
    ReleasesJsonDeleteError,
    ReleasesJsonLoadError,
    ReleasesJsonNotFound,
    ReleasesJsonSaveError,
)
from dbnomics_data_model.storage.adapters.filesystem.file_utils import iter_child_directories
from dbnomics_data_model.storage.adapters.filesystem.git.git_provider_directory_manager import (
    GitProviderDirectoryManager,
)
from dbnomics_data_model.storage.adapters.filesystem.model.provider_json import ProviderJson
from dbnomics_data_model.storage.adapters.filesystem.variants.json_lines.json_lines_dataset_directory_manager import (
    JsonLinesDatasetDirectoryManager,
)
from dbnomics_data_model.storage.adapters.filesystem.variants.tsv.tsv_dataset_directory_manager import (
    TsvDatasetDirectoryManager,
)
from dbnomics_data_model.storage.errors.category_tree import (
    CategoryTreeDeleteError,
    CategoryTreeLoadError,
    CategoryTreeNotFound,
    CategoryTreeSaveError,
)
from dbnomics_data_model.storage.errors.dataset import DatasetDeleteError, DatasetNotFound
from dbnomics_data_model.storage.errors.dataset_releases import (
    DatasetReleasesDeleteError,
    DatasetReleasesLoadError,
    DatasetReleasesNotFound,
    DatasetReleasesSaveError,
)
from dbnomics_data_model.storage.errors.provider_metadata import (
    ProviderMetadataDeleteError,
    ProviderMetadataLoadError,
    ProviderMetadataNotFound,
    ProviderMetadataSaveError,
)
from dbnomics_data_model.storage.errors.revisions import LatestRevisionOnlyOperation, RevisionsNotAvailable
from dbnomics_data_model.storage.errors.series import SeriesLoadError, SeriesNotFound

from .constants import CATEGORY_TREE_JSON, DATASET_JSON, PROVIDER_JSON, RELEASES_JSON, UNKNOWN_PROVIDER_CODE
from .errors.category_tree_json_file import (
    CategoryTreeJsonDeleteError,
    CategoryTreeJsonLoadError,
    CategoryTreeJsonNotFound,
    CategoryTreeJsonSaveError,
)
from .errors.dataset_directory import DatasetDirectoryDeleteError, DatasetDirectoryNotFound
from .errors.provider_directory import ProviderDirectoryNotFound
from .errors.provider_json_file import (
    ProviderJsonDeleteError,
    ProviderJsonLoadError,
    ProviderJsonNotFound,
    ProviderJsonSaveError,
)
from .model.category_tree_json import CategoryTreeJson
from .model.releases_json import DatasetReleasesJson, ReleasesJson
from .storage_variant import StorageVariant
from .variants.json_lines.offsets.repo import JsonLinesSeriesOffsetRepo

__all__ = ["ProviderDirectoryManager", "create_provider_directory_manager"]


logger = daiquiri.getLogger(__name__)


class ProviderDirectoryManager:
    def __init__(
        self,
        *,
        default_storage_variant: StorageVariant | None = None,
        git_provider_directory_manager: GitProviderDirectoryManager | None = None,
        provider_code: ProviderCode,
        provider_dir: Path | str,
        series_offset_repo: JsonLinesSeriesOffsetRepo | None = None,
    ) -> None:
        if default_storage_variant is None:
            default_storage_variant = StorageVariant.JSON_LINES
        self.default_storage_variant = default_storage_variant

        self.provider_code = provider_code

        if isinstance(provider_dir, str):
            provider_dir = Path(provider_dir)
        if not provider_dir.is_dir():
            raise ProviderDirectoryNotFound(provider_code=provider_code, provider_dir=provider_dir)
        self.provider_dir = provider_dir

        if git_provider_directory_manager is None:
            with contextlib.suppress(GitProviderDirectoryManagerError):
                git_provider_directory_manager = GitProviderDirectoryManager.open(provider_dir)
        self._git_provider_directory_manager = git_provider_directory_manager

        self._series_offset_repo = series_offset_repo

    @classmethod
    def open(
        cls,
        provider_dir: Path | str,
        *,
        default_storage_variant: StorageVariant | None = None,
        series_offset_repo: JsonLinesSeriesOffsetRepo | None = None,
    ) -> "ProviderDirectoryManager":
        instance = ProviderDirectoryManager(
            provider_code=UNKNOWN_PROVIDER_CODE,
            provider_dir=provider_dir,
            default_storage_variant=default_storage_variant,
            series_offset_repo=series_offset_repo,
        )
        provider_code = instance.load_provider_code()
        instance.provider_code = provider_code
        return instance

    @property
    def category_tree_json_path(self) -> Path:
        return self.provider_dir / CATEGORY_TREE_JSON

    def create_dataset_directory_manager(
        self, dataset_code: DatasetCode, *, ensure_dir: bool = False, revision_id: RevisionId | None = None
    ) -> JsonLinesDatasetDirectoryManager | TsvDatasetDirectoryManager:
        dataset_dir = self.get_dataset_dir(dataset_code)
        if ensure_dir:
            if revision_id is not None:
                raise LatestRevisionOnlyOperation(revision_id=revision_id)
            dataset_dir.mkdir(exist_ok=True)

        dataset_id = DatasetId(self.provider_code, dataset_code)

        try:
            return create_dataset_directory_manager(
                dataset_dir=dataset_dir,
                dataset_id=dataset_id,
                default_storage_variant=self.default_storage_variant,
                git_provider_directory_manager=self._git_provider_directory_manager,
                revision_id=revision_id,
                series_offset_repo=self._series_offset_repo,
            )
        except DatasetDirectoryNotFound as exc:
            raise DatasetNotFound(dataset_id=dataset_id) from exc

    def delete_category_tree(self, *, missing_ok: bool = False) -> None:
        try:
            self.delete_category_tree_json(missing_ok=missing_ok)
        except CategoryTreeJsonDeleteError as exc:
            raise CategoryTreeDeleteError(provider_code=self.provider_code) from exc
        except CategoryTreeJsonNotFound as exc:
            raise CategoryTreeNotFound(provider_code=self.provider_code) from exc

    def delete_category_tree_json(self, *, missing_ok: bool = False) -> None:
        category_tree_json_path = self.category_tree_json_path

        try:
            category_tree_json_path.unlink(missing_ok=missing_ok)
        except FileNotFoundError as exc:
            raise CategoryTreeJsonNotFound(
                category_tree_json_path=category_tree_json_path, provider_code=self.provider_code
            ) from exc
        except Exception as exc:
            raise CategoryTreeJsonDeleteError(
                category_tree_json_path=category_tree_json_path, provider_code=self.provider_code
            ) from exc

    def delete_dataset(self, dataset_code: DatasetCode, *, missing_ok: bool = False) -> None:
        dataset_id = DatasetId(self.provider_code, dataset_code)
        try:
            self.delete_dataset_dir(dataset_code, missing_ok=missing_ok)
        except DatasetDirectoryDeleteError as exc:
            raise DatasetDeleteError(dataset_id=dataset_id) from exc
        except DatasetDirectoryNotFound as exc:
            raise DatasetNotFound(dataset_id=dataset_id) from exc

    def delete_dataset_dir(self, dataset_code: DatasetCode, *, missing_ok: bool = False) -> None:
        dataset_dir = self.get_dataset_dir(dataset_code)
        dataset_id = DatasetId(self.provider_code, dataset_code)

        if not dataset_dir.is_dir():
            if not missing_ok:
                raise DatasetDirectoryNotFound(dataset_dir=dataset_dir, dataset_id=dataset_id)
            return

        try:
            shutil.rmtree(dataset_dir)
        except Exception as exc:
            raise DatasetDirectoryDeleteError(dataset_dir=dataset_dir, dataset_id=dataset_id) from exc

    def delete_dataset_metadata(self, dataset_code: DatasetCode, *, missing_ok: bool = False) -> None:
        dataset_directory_manager = self.create_dataset_directory_manager(dataset_code)
        dataset_directory_manager.delete_dataset_metadata(missing_ok=missing_ok)

    def delete_dataset_releases(self, *, missing_ok: bool = False) -> None:
        try:
            self.delete_releases_json(missing_ok=missing_ok)
        except ReleasesJsonDeleteError as exc:
            raise DatasetReleasesDeleteError(provider_code=self.provider_code) from exc
        except ReleasesJsonNotFound as exc:
            raise DatasetReleasesNotFound(provider_code=self.provider_code) from exc

    def delete_provider_json(self, *, missing_ok: bool = False) -> None:
        provider_json_path = self.provider_json_path
        try:
            provider_json_path.unlink(missing_ok=missing_ok)
        except FileNotFoundError as exc:
            raise ProviderJsonNotFound(provider_code=self.provider_code, provider_json_path=provider_json_path) from exc
        except Exception as exc:
            raise ProviderJsonDeleteError(
                provider_code=self.provider_code, provider_json_path=provider_json_path
            ) from exc

    def delete_provider_metadata(self, *, missing_ok: bool = False) -> None:
        try:
            self.delete_provider_json(missing_ok=missing_ok)
        except ProviderJsonDeleteError as exc:
            raise ProviderMetadataDeleteError(provider_code=self.provider_code) from exc
        except ProviderJsonNotFound as exc:
            raise ProviderMetadataNotFound(provider_code=self.provider_code) from exc

    def delete_releases_json(self, *, missing_ok: bool = False) -> None:
        releases_json_path = self.releases_json_path

        try:
            releases_json_path.unlink(missing_ok=missing_ok)
        except FileNotFoundError as exc:
            raise ReleasesJsonNotFound(provider_code=self.provider_code, releases_json_path=releases_json_path) from exc
        except Exception as exc:
            raise ReleasesJsonDeleteError(
                provider_code=self.provider_code, releases_json_path=releases_json_path
            ) from exc

    def delete_dataset_series(self, dataset_code: DatasetCode, *, missing_ok: bool = False) -> None:
        dataset_directory_manager = self.create_dataset_directory_manager(dataset_code)
        dataset_directory_manager.delete_series(missing_ok=missing_ok)

    def get_dataset_dir(self, dataset_code: DatasetCode) -> Path:
        return self.provider_dir / str(dataset_code)

    def has_dataset(self, dataset_code: DatasetCode, *, revision_id: RevisionId | None = None) -> bool:
        return self.has_dataset_metadata(dataset_code, revision_id=revision_id)

    def has_dataset_metadata(self, dataset_code: DatasetCode, *, revision_id: RevisionId | None = None) -> bool:
        try:
            dataset_directory_manager = self.create_dataset_directory_manager(dataset_code, revision_id=revision_id)
        except DatasetNotFound:
            return False

        return dataset_directory_manager.has_dataset_metadata()

    def has_series(
        self, series_code: SeriesCode, *, dataset_code: DatasetCode, revision_id: RevisionId | None = None
    ) -> bool:
        dataset_directory_manager = self.create_dataset_directory_manager(dataset_code, revision_id=revision_id)
        return dataset_directory_manager.has_series(series_code)

    def iter_dataset_codes(self, *, revision_id: RevisionId | None = None) -> Iterator[DatasetCode]:
        for dataset_code, _ in self.iter_dataset_directories(revision_id=revision_id):
            yield dataset_code

    def iter_dataset_directories(self, *, revision_id: RevisionId | None = None) -> Iterator[tuple[DatasetCode, Path]]:
        if revision_id is None:
            child_directories_iter = self._iter_dataset_directories()
        else:
            if self._git_provider_directory_manager is None:
                raise RevisionsNotAvailable

            child_directories_iter = self._git_provider_directory_manager.iter_dataset_directories(
                revision_id=revision_id
            )

        yield from child_directories_iter

    def iter_dataset_releases(self, *, revision_id: RevisionId | None = None) -> Iterator[DatasetReleases]:
        try:
            releases_json = self.load_releases_json(revision_id=revision_id)
        except ReleasesJsonLoadError as exc:
            raise DatasetReleasesLoadError(provider_code=self.provider_code) from exc

        if releases_json is None:
            return

        for dataset_releases_json in releases_json.dataset_releases:
            try:
                yield dataset_releases_json.to_domain_model()
            except DataModelError as exc:
                raise DatasetReleasesLoadError(provider_code=self.provider_code) from exc

    def iter_dataset_series(
        self,
        dataset_code: DatasetCode,
        *,
        revision_id: RevisionId | None = None,
        series_codes: Iterable[SeriesCode] | None = None,
        with_observations: bool = True,
    ) -> Iterator[Series]:
        dataset_directory_manager = self.create_dataset_directory_manager(dataset_code, revision_id=revision_id)
        yield from dataset_directory_manager.iter_series(series_codes=series_codes, with_observations=with_observations)

    def iter_series_changes(
        self, series_code: SeriesCode, *, dataset_code: DatasetCode, start_revision_id: RevisionId | None = None
    ) -> Iterator[tuple[Revision, DataPatch]]:
        if self._git_provider_directory_manager is None:
            raise RevisionsNotAvailable

        series_id = SeriesId(self.provider_code, dataset_code, series_code)

        dataset_directory_manager_cache: dict[
            tuple[str, str], JsonLinesDatasetDirectoryManager | TsvDatasetDirectoryManager
        ] = {}

        def get_or_create_dataset_directory_manager(
            dataset_code: DatasetCode, *, repo_revision_id: RevisionId
        ) -> JsonLinesDatasetDirectoryManager | TsvDatasetDirectoryManager:
            key = (str(dataset_code), repo_revision_id)
            dataset_directory_manager = dataset_directory_manager_cache.get(key)
            if dataset_directory_manager is not None:
                return dataset_directory_manager

            dataset_directory_manager = self.create_dataset_directory_manager(
                dataset_code, revision_id=repo_revision_id
            )
            dataset_directory_manager_cache[key] = dataset_directory_manager
            return dataset_directory_manager

        for repo_revision, parent_repo_revision in iter_revision_pairs(
            self._git_provider_directory_manager.iter_repo_revisions(start_revision_id=start_revision_id)
        ):
            logger.debug("Determining if the series %r changed at revision %r", str(series_id), repo_revision.id)

            dataset_directory_manager = get_or_create_dataset_directory_manager(
                dataset_code, repo_revision_id=repo_revision.id
            )

            try:
                series = dataset_directory_manager.load_series(series_code)
            except SeriesNotFound:
                logger.debug("Series %r was not found at revision %r", str(series_id), repo_revision.id)
                continue
            except SeriesLoadError:
                logger.exception("Could not load series %r from revision %r", str(series_id), repo_revision.id)
                continue

            previous_series: Series | None = None
            if isinstance(parent_repo_revision, Revision):
                previous_dataset_directory_manager = get_or_create_dataset_directory_manager(
                    dataset_code, repo_revision_id=parent_repo_revision.id
                )

                try:
                    previous_series = previous_dataset_directory_manager.load_series(series_code)
                except SeriesNotFound:
                    logger.debug(
                        "Series %r was not found at parent revision %r", str(series_id), parent_repo_revision.id
                    )
                    continue
                except SeriesLoadError:
                    logger.exception(
                        "Could not load series %r from parent revision %r", str(series_id), parent_repo_revision.id
                    )
                    continue

            differ = DataDiffer()
            series_patch = differ.diff(previous_series, series)
            if not series_patch.changes:
                logger.debug("Series %r did not change at revision %r", str(series_id), repo_revision.id)
                continue

            metadata = dataset_directory_manager.get_revision_metadata_for_series(series_code)
            revision = replace(repo_revision, metadata=metadata)

            logger.debug("Series %r changed at revision %r", str(series_id), repo_revision.id)
            yield revision, series_patch

    def load_category_tree(self, *, revision_id: RevisionId | None = None) -> CategoryTree | None:
        try:
            category_tree_json = self.load_category_tree_json(revision_id=revision_id)
        except CategoryTreeJsonLoadError as exc:
            raise CategoryTreeLoadError(provider_code=self.provider_code) from exc

        if category_tree_json is None:
            return None

        try:
            return category_tree_json.to_domain_model()
        except DataModelError as exc:
            raise CategoryTreeLoadError(provider_code=self.provider_code) from exc

    def load_category_tree_json(self, *, revision_id: RevisionId | None = None) -> CategoryTreeJson | None:
        category_tree_json_path = self.category_tree_json_path

        category_tree_json_data = (
            self._load_category_tree_json_data_from_file()
            if revision_id is None
            else self._load_category_tree_json_data_from_git(revision_id=revision_id)
        )

        if category_tree_json_data is None:
            return None

        try:
            return CategoryTreeJson.from_json_data(category_tree_json_data)
        except JsonModelError as exc:
            raise CategoryTreeJsonLoadError(
                category_tree_json_path=category_tree_json_path, provider_code=self.provider_code
            ) from exc

    def load_dataset_metadata(
        self, dataset_code: DatasetCode, *, revision_id: RevisionId | None = None
    ) -> DatasetMetadata:
        dataset_directory_manager = self.create_dataset_directory_manager(dataset_code, revision_id=revision_id)
        return dataset_directory_manager.load_dataset_metadata()

    def load_provider_code(self) -> ProviderCode:
        provider_metadata = self.load_provider_metadata()
        return provider_metadata.code

    def load_provider_json(self, *, revision_id: RevisionId | None = None) -> ProviderJson:
        provider_json_path = self.provider_json_path

        provider_json_data = (
            self._load_provider_json_data_from_file()
            if revision_id is None
            else self._load_provider_json_data_from_git(revision_id=revision_id)
        )

        try:
            provider_json = ProviderJson.from_json_data(provider_json_data)
        except JsonModelError as exc:
            raise ProviderJsonLoadError(
                provider_code=self.provider_code, provider_json_path=provider_json_path
            ) from exc

        try:
            self._validate_provider_json_code_matches(provider_json)
        except ProviderJsonCodeMismatch as exc:
            raise ProviderJsonLoadError(
                provider_code=self.provider_code, provider_json_path=provider_json_path
            ) from exc

        return provider_json

    def load_provider_metadata(self, *, revision_id: RevisionId | None = None) -> ProviderMetadata:
        try:
            provider_json = self.load_provider_json(revision_id=revision_id)
        except ProviderJsonNotFound as exc:
            raise ProviderMetadataNotFound(provider_code=self.provider_code) from exc
        except ProviderJsonLoadError as exc:
            raise ProviderMetadataLoadError(provider_code=self.provider_code) from exc

        try:
            provider_metadata = provider_json.to_domain_model()
        except DataModelError as exc:
            raise ProviderMetadataLoadError(provider_code=self.provider_code) from exc

        try:
            self._validate_provider_metadata_code_matches(provider_metadata)
        except ProviderMetadataCodeMismatch as exc:
            raise ProviderMetadataLoadError(provider_code=self.provider_code) from exc

        return provider_metadata

    def load_releases_json(self, *, revision_id: RevisionId | None = None) -> ReleasesJson | None:
        releases_json_data = (
            self._load_releases_json_data_from_file()
            if revision_id is None
            else self._load_releases_json_data_from_git(revision_id=revision_id)
        )

        if releases_json_data is None:
            return None

        try:
            return ReleasesJson.from_json_data(releases_json_data)
        except JsonModelError as exc:
            raise ReleasesJsonLoadError(
                provider_code=self.provider_code, releases_json_path=self.releases_json_path
            ) from exc

    def load_series(
        self,
        series_code: SeriesCode,
        *,
        dataset_code: DatasetCode,
        revision_id: RevisionId | None = None,
        with_observations: bool = True,
    ) -> Series:
        dataset_directory_manager = self.create_dataset_directory_manager(dataset_code, revision_id=revision_id)
        return dataset_directory_manager.load_series(series_code, with_observations=with_observations)

    @property
    def provider_json_path(self) -> Path:
        return self.provider_dir / PROVIDER_JSON

    @property
    def releases_json_path(self) -> Path:
        return self.provider_dir / RELEASES_JSON

    def save_category_tree(self, category_tree: CategoryTree) -> None:
        category_tree_json = CategoryTreeJson.from_domain_model(category_tree)
        try:
            self.save_category_tree_json(category_tree_json)
        except CategoryTreeJsonSaveError as exc:
            raise CategoryTreeSaveError(category_tree=category_tree, provider_code=self.provider_code) from exc

    def save_category_tree_json(self, category_tree_json: CategoryTreeJson) -> None:
        category_tree_json_path = self.category_tree_json_path

        category_tree_json_data = category_tree_json.to_json_data()

        try:
            save_json_file(category_tree_json_path, category_tree_json_data)
        except JsonError as exc:
            raise CategoryTreeJsonSaveError(
                category_tree_json=category_tree_json,
                category_tree_json_path=category_tree_json_path,
                provider_code=self.provider_code,
            ) from exc

    def save_dataset_metadata(self, dataset_metadata: DatasetMetadata) -> None:
        dataset_code = dataset_metadata.code
        dataset_directory_manager = self.create_dataset_directory_manager(dataset_code, ensure_dir=True)
        dataset_directory_manager.save_dataset_metadata(dataset_metadata)

    def save_dataset_releases(self, dataset_releases: DatasetReleases | Iterable[DatasetReleases]) -> None:
        dataset_releases_list = (
            [dataset_releases] if isinstance(dataset_releases, DatasetReleases) else list(dataset_releases)
        )
        dataset_releases_json_list = [
            DatasetReleasesJson.from_domain_model(dataset_releases) for dataset_releases in dataset_releases_list
        ]
        releases_json = ReleasesJson(dataset_releases=dataset_releases_json_list)
        try:
            self.save_releases_json(releases_json)
        except ReleasesJsonSaveError as exc:
            raise DatasetReleasesSaveError(
                dataset_releases_list=dataset_releases_list, provider_code=self.provider_code
            ) from exc

    def save_provider_json(self, provider_json: ProviderJson) -> None:
        self._validate_provider_json_code_matches(provider_json)

        provider_json_path = self.provider_json_path
        provider_json_data = provider_json.to_json_data()

        try:
            save_json_file(provider_json_path, provider_json_data)
        except JsonError as exc:
            raise ProviderJsonSaveError(
                provider_code=self.provider_code, provider_json=provider_json, provider_json_path=provider_json_path
            ) from exc

        logger.info("Saved provider metadata to %s", format_file_path_with_size(provider_json_path))

    def save_provider_metadata(self, provider_metadata: ProviderMetadata) -> None:
        self._validate_provider_metadata_code_matches(provider_metadata)

        provider_json = ProviderJson.from_domain_model(provider_metadata)

        try:
            self.save_provider_json(provider_json)
        except ProviderJsonSaveError as exc:
            raise ProviderMetadataSaveError(
                provider_code=self.provider_code, provider_metadata=provider_metadata
            ) from exc

    def save_releases_json(self, releases_json: ReleasesJson) -> None:
        releases_json_path = self.releases_json_path

        try:
            save_json_file(releases_json_path, releases_json.to_json_data())
        except JsonError as exc:
            raise ReleasesJsonSaveError(
                provider_code=self.provider_code, releases_json=releases_json, releases_json_path=releases_json_path
            ) from exc

    def save_series(self, series: Series | Iterable[Series], *, dataset_code: DatasetCode) -> None:
        dataset_directory_manager = self.create_dataset_directory_manager(dataset_code, ensure_dir=True)
        dataset_directory_manager.save_series(series)

    def _iter_dataset_directories(self) -> Iterator[tuple[DatasetCode, Path]]:
        for child_dir in iter_child_directories(self.provider_dir):
            if not (child_dir / DATASET_JSON).is_file():
                logger.debug("Ignoring directory without a %r file", DATASET_JSON, child_dir=child_dir)
                continue

            dir_name = child_dir.name

            try:
                dataset_code = DatasetCode.parse(dir_name)
            except DatasetCodeParseError:
                logger.exception("Ignoring directory which name is not a dataset code", dir_name=dir_name)
                continue

            yield dataset_code, child_dir

    def _load_category_tree_json_data_from_file(self) -> Json | None:
        category_tree_json_path = self.category_tree_json_path

        try:
            return parse_json_file(category_tree_json_path)
        except FileNotFoundError:
            return None
        except JsonParseError as exc:
            raise CategoryTreeJsonLoadError(
                category_tree_json_path=category_tree_json_path, provider_code=self.provider_code
            ) from exc

    def _load_category_tree_json_data_from_git(self, *, revision_id: RevisionId) -> Json | None:
        if self._git_provider_directory_manager is None:
            raise RevisionsNotAvailable

        category_tree_json_path = self.category_tree_json_path

        try:
            return self._git_provider_directory_manager.load_json_file(category_tree_json_path, revision_id=revision_id)
        except BlobNotFound:
            return None
        except JsonParseError as exc:
            raise CategoryTreeJsonLoadError(
                category_tree_json_path=category_tree_json_path, provider_code=self.provider_code
            ) from exc

    def _load_provider_json_data_from_file(self) -> Json:
        provider_json_path = self.provider_json_path

        try:
            return parse_json_file(provider_json_path)
        except FileNotFoundError as exc:
            raise ProviderJsonNotFound(provider_code=self.provider_code, provider_json_path=provider_json_path) from exc
        except JsonParseError as exc:
            raise ProviderJsonLoadError(
                provider_code=self.provider_code, provider_json_path=provider_json_path
            ) from exc

    def _load_provider_json_data_from_git(self, *, revision_id: RevisionId) -> Json:
        if self._git_provider_directory_manager is None:
            raise RevisionsNotAvailable

        provider_json_path = self.provider_json_path

        try:
            return self._git_provider_directory_manager.load_json_file(provider_json_path, revision_id=revision_id)
        except BlobNotFound as exc:
            raise ProviderJsonNotFound(provider_code=self.provider_code, provider_json_path=provider_json_path) from exc
        except JsonParseError as exc:
            raise ProviderJsonLoadError(
                provider_code=self.provider_code, provider_json_path=provider_json_path
            ) from exc

    def _load_releases_json_data_from_file(self) -> Json | None:
        releases_json_path = self.releases_json_path

        try:
            return parse_json_file(releases_json_path)
        except FileNotFoundError:
            return None
        except JsonParseError as exc:
            raise ReleasesJsonLoadError(
                provider_code=self.provider_code, releases_json_path=releases_json_path
            ) from exc

    def _load_releases_json_data_from_git(self, *, revision_id: RevisionId) -> Json | None:
        if self._git_provider_directory_manager is None:
            raise RevisionsNotAvailable

        releases_json_path = self.releases_json_path

        try:
            return self._git_provider_directory_manager.load_json_file(releases_json_path, revision_id=revision_id)
        except BlobNotFound:
            return None
        except JsonParseError as exc:
            raise ReleasesJsonLoadError(
                provider_code=self.provider_code, releases_json_path=releases_json_path
            ) from exc

    def _validate_provider_json_code_matches(self, provider_json: ProviderJson) -> None:
        if self.provider_code is UNKNOWN_PROVIDER_CODE:
            return

        if provider_json.code != self.provider_code:
            raise ProviderJsonCodeMismatch(expected_provider_code=self.provider_code, provider_json=provider_json)

    def _validate_provider_metadata_code_matches(self, provider_metadata: ProviderMetadata) -> None:
        if self.provider_code is UNKNOWN_PROVIDER_CODE:
            return

        if provider_metadata.code != self.provider_code:
            raise ProviderMetadataCodeMismatch(
                expected_provider_code=self.provider_code, provider_metadata=provider_metadata
            )


@lru_cache
def create_provider_directory_manager(
    *,
    default_storage_variant: StorageVariant,
    provider_code: ProviderCode,
    provider_dir: Path,
    series_offset_repo: JsonLinesSeriesOffsetRepo | None,
) -> ProviderDirectoryManager:
    return ProviderDirectoryManager(
        provider_code=provider_code,
        provider_dir=provider_dir,
        default_storage_variant=default_storage_variant,
        series_offset_repo=series_offset_repo,
    )
