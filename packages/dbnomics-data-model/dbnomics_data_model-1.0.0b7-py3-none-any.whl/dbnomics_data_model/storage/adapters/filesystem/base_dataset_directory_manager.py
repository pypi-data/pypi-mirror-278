from abc import ABC, abstractmethod
from collections.abc import Iterable, Iterator
from functools import lru_cache
from pathlib import Path
from typing import TYPE_CHECKING, Generic, TypeVar, assert_never

from jsonalias import Json

from dbnomics_data_model.errors import DataModelError
from dbnomics_data_model.json_utils import save_json_file
from dbnomics_data_model.json_utils.errors import JsonError, JsonParseError
from dbnomics_data_model.json_utils.parsing import parse_json_file
from dbnomics_data_model.model import DatasetCode, DatasetId, DatasetMetadata, Series, SeriesCode
from dbnomics_data_model.model.errors.dataset_metadata import DatasetMetadataCodeMismatch
from dbnomics_data_model.model.identifiers import ProviderCode, SeriesId
from dbnomics_data_model.model.revisions.types import RevisionId, RevisionMetadata
from dbnomics_data_model.storage.adapters.filesystem.errors.dataset_directory_manager import (
    DatasetDirectoryNameMismatch,
    DatasetJsonCodeMismatch,
)
from dbnomics_data_model.storage.adapters.filesystem.errors.dataset_json_file import (
    DatasetJsonLoadError,
    DatasetJsonNotFound,
    DatasetJsonSaveError,
)
from dbnomics_data_model.storage.adapters.filesystem.errors.git_provider_directory_manager import BlobNotFound
from dbnomics_data_model.storage.adapters.filesystem.errors.json_model import JsonModelError
from dbnomics_data_model.storage.adapters.filesystem.git.git_provider_directory_manager import (
    GitProviderDirectoryManager,
)
from dbnomics_data_model.storage.adapters.filesystem.model.errors.base_dataset_json import DatasetJsonError
from dbnomics_data_model.storage.adapters.filesystem.storage_variant import StorageVariant
from dbnomics_data_model.storage.adapters.filesystem.variants.json_lines.offsets.repo import JsonLinesSeriesOffsetRepo
from dbnomics_data_model.storage.errors.dataset import DatasetSomeSeriesNotFound, DatasetStorageError
from dbnomics_data_model.storage.errors.dataset_metadata import DatasetMetadataLoadError, DatasetMetadataNotFound
from dbnomics_data_model.storage.errors.revisions import LatestRevisionOnlyOperation, RevisionsNotAvailable
from dbnomics_data_model.storage.errors.series import SeriesLoadError, SeriesNotFound
from dbnomics_data_model.utils import raise_first_error
from dbnomics_data_model.validation.validation_settings import overridden_validation_settings

from .constants import DATASET_JSON
from .errors.dataset_directory import DatasetDirectoryNotFound

if TYPE_CHECKING:
    from dbnomics_data_model.storage.adapters.filesystem.variants.json_lines.json_lines_dataset_directory_manager import (
        JsonLinesDatasetDirectoryManager,
    )
    from dbnomics_data_model.storage.adapters.filesystem.variants.tsv.tsv_dataset_directory_manager import (
        TsvDatasetDirectoryManager,
    )

    from .model.base_dataset_json import BaseDatasetJson

__all__ = ["BaseDatasetDirectoryManager", "create_dataset_directory_manager"]


TDatasetJson = TypeVar("TDatasetJson", bound="BaseDatasetJson")


class BaseDatasetDirectoryManager(ABC, Generic[TDatasetJson]):
    def __init__(
        self,
        *,
        dataset_dir: Path | str,
        dataset_id: DatasetId,
        git_provider_directory_manager: GitProviderDirectoryManager | None,
        revision_id: RevisionId | None = None,
    ) -> None:
        if isinstance(dataset_dir, str):
            dataset_dir = Path(dataset_dir)
        if revision_id is None:
            if not dataset_dir.is_dir():
                raise DatasetDirectoryNotFound(dataset_dir=dataset_dir, dataset_id=dataset_id)
        else:
            if git_provider_directory_manager is None:
                raise RevisionsNotAvailable
            if not git_provider_directory_manager.has_dir(dataset_dir, revision_id=revision_id):
                raise DatasetDirectoryNotFound(dataset_dir=dataset_dir, dataset_id=dataset_id)
        self.dataset_dir = dataset_dir

        self.dataset_id = dataset_id
        self.revision_id = revision_id

        self._git_provider_directory_manager = git_provider_directory_manager

        self._validate()

    @property
    def dataset_code(self) -> DatasetCode:
        return self.dataset_id.dataset_code

    @property
    @abstractmethod
    def dataset_json_class(self) -> type[TDatasetJson]: ...

    @property
    def dataset_json_path(self) -> Path:
        return self.dataset_dir / DATASET_JSON

    @abstractmethod
    def delete_dataset_metadata(self, *, missing_ok: bool = False) -> None: ...

    @abstractmethod
    def delete_series(self, *, missing_ok: bool = False) -> None:
        """Delete all the series of the dataset."""

    @abstractmethod
    def get_revision_metadata_for_series(self, series_code: SeriesCode) -> RevisionMetadata: ...

    def has_dataset_metadata(self) -> bool:
        try:
            self.load_dataset_metadata()
        except DatasetMetadataNotFound:
            return False

        return True

    def has_series(self, series_code: SeriesCode) -> bool:
        with overridden_validation_settings(disable_series_validation=True):
            try:
                self.load_series(series_code, with_observations=False)
            except SeriesNotFound:
                return False
            return True

    @abstractmethod
    def iter_series(
        self,
        *,
        series_codes: Iterable[SeriesCode] | None = None,
        with_observations: bool = True,
    ) -> Iterator[Series]: ...

    def load_dataset_json(self, *, validate: bool = False) -> TDatasetJson:
        dataset_json_path = self.dataset_json_path

        dataset_json_data = (
            self._load_dataset_json_data_from_file(dataset_json_path)
            if self.revision_id is None
            else self._load_dataset_json_data_from_git(dataset_json_path)
        )

        try:
            dataset_json = self.dataset_json_class.from_json_data(dataset_json_data)
        except JsonModelError as exc:
            raise DatasetJsonLoadError(
                dataset_id=self.dataset_id, dataset_json_path=dataset_json_path, revision_id=self.revision_id
            ) from exc

        try:
            self._validate_dataset_json_code_matches(dataset_json)
        except DatasetJsonCodeMismatch as exc:
            raise DatasetJsonLoadError(
                dataset_id=self.dataset_id, dataset_json_path=dataset_json_path, revision_id=self.revision_id
            ) from exc

        if validate:
            raise_first_error(dataset_json.validate())

        return dataset_json

    def load_dataset_metadata(self) -> DatasetMetadata:
        try:
            dataset_json = self.load_dataset_json(validate=True)
        except DatasetJsonNotFound as exc:
            raise DatasetMetadataNotFound(dataset_id=self.dataset_id, revision_id=self.revision_id) from exc
        except (DatasetJsonLoadError, DatasetJsonError) as exc:
            raise DatasetMetadataLoadError(dataset_id=self.dataset_id, revision_id=self.revision_id) from exc

        try:
            dataset_metadata = dataset_json.to_domain_model()
        except DataModelError as exc:
            raise DatasetMetadataLoadError(dataset_id=self.dataset_id, revision_id=self.revision_id) from exc

        try:
            self._validate_dataset_metadata_code_matches(dataset_metadata)
        except DatasetMetadataCodeMismatch as exc:
            raise DatasetMetadataLoadError(dataset_id=self.dataset_id, revision_id=self.revision_id) from exc

        return dataset_metadata

    def load_series(self, series_code: SeriesCode, *, with_observations: bool = True) -> Series:
        series_id = SeriesId.from_dataset_id(self.dataset_id, series_code)
        series_iter = self.iter_series(series_codes=[series_code], with_observations=with_observations)
        try:
            return next(series_iter)
        except StopIteration as exc:
            raise SeriesNotFound(revision_id=self.revision_id, series_id=series_id) from exc
        except DatasetSomeSeriesNotFound as exc:
            raise SeriesNotFound(revision_id=self.revision_id, series_id=series_id) from exc
        except DatasetStorageError as exc:
            raise SeriesLoadError(revision_id=self.revision_id, series_id=series_id) from exc

    @abstractmethod
    def matches_variant(self, *, revision_id: RevisionId | None = None) -> bool: ...

    @property
    def provider_code(self) -> ProviderCode:
        return self.dataset_id.provider_code

    def save_dataset_json(self, dataset_json: TDatasetJson) -> None:
        if self.revision_id is not None:
            raise LatestRevisionOnlyOperation(revision_id=self.revision_id)

        self._validate_dataset_json_code_matches(dataset_json)

        dataset_json_path = self.dataset_json_path
        dataset_json_data = dataset_json.to_json_data()

        try:
            save_json_file(dataset_json_path, dataset_json_data)
        except JsonError as exc:
            raise DatasetJsonSaveError(dataset_id=self.dataset_id, dataset_json_path=dataset_json_path) from exc

    @abstractmethod
    def save_dataset_metadata(self, dataset_metadata: DatasetMetadata) -> None: ...

    @abstractmethod
    def save_series(self, series: Series | Iterable[Series]) -> None: ...

    @property
    @abstractmethod
    def storage_variant(self) -> StorageVariant: ...

    def _load_dataset_json_data_from_file(self, dataset_json_path: Path) -> Json:
        if self.revision_id is not None:
            raise LatestRevisionOnlyOperation(revision_id=self.revision_id)

        try:
            return parse_json_file(dataset_json_path)
        except FileNotFoundError as exc:
            raise DatasetJsonNotFound(dataset_id=self.dataset_id, dataset_json_path=dataset_json_path) from exc
        except JsonParseError as exc:
            raise DatasetJsonLoadError(dataset_id=self.dataset_id, dataset_json_path=dataset_json_path) from exc

    def _load_dataset_json_data_from_git(self, dataset_json_path: Path) -> Json:
        if self._git_provider_directory_manager is None:
            raise RevisionsNotAvailable

        if self.revision_id is None:
            msg = "When self.revisions is None here, it means reading from the file-system, not Git"
            raise RuntimeError(msg)

        try:
            return self._git_provider_directory_manager.load_json_file(dataset_json_path, revision_id=self.revision_id)
        except BlobNotFound as exc:
            raise DatasetJsonNotFound(
                dataset_id=self.dataset_id, dataset_json_path=dataset_json_path, revision_id=self.revision_id
            ) from exc
        except JsonParseError as exc:
            raise DatasetJsonLoadError(
                dataset_id=self.dataset_id, dataset_json_path=dataset_json_path, revision_id=self.revision_id
            ) from exc

    def _validate(self) -> None:
        if self.dataset_dir.name != str(self.dataset_code):
            raise DatasetDirectoryNameMismatch(dataset_code=self.dataset_code, dataset_dir=self.dataset_dir)

        # Just load dataset.json to see if its code matches self.dataset_code
        try:
            self.load_dataset_json()
        except DatasetJsonNotFound:
            return
        except DatasetJsonLoadError as exc:
            raise DatasetMetadataLoadError(dataset_id=self.dataset_id, revision_id=self.revision_id) from exc

    def _validate_dataset_json_code_matches(self, dataset_json: "BaseDatasetJson") -> None:
        dataset_code = self.dataset_code
        if dataset_json.code != str(dataset_code):
            raise DatasetJsonCodeMismatch(dataset_json=dataset_json, expected_dataset_code=dataset_code)

    def _validate_dataset_metadata_code_matches(self, dataset_metadata: DatasetMetadata) -> None:
        dataset_code = self.dataset_id.dataset_code
        if dataset_metadata.code != dataset_code:
            raise DatasetMetadataCodeMismatch(dataset_metadata=dataset_metadata, expected_dataset_code=dataset_code)


@lru_cache
def create_dataset_directory_manager(
    *,
    dataset_dir: Path,
    dataset_id: DatasetId,
    default_storage_variant: StorageVariant,
    git_provider_directory_manager: GitProviderDirectoryManager | None,
    revision_id: RevisionId | None,
    series_offset_repo: JsonLinesSeriesOffsetRepo | None,
) -> "JsonLinesDatasetDirectoryManager | TsvDatasetDirectoryManager":
    def create_for_storage_variant(
        storage_variant: StorageVariant,
    ) -> "JsonLinesDatasetDirectoryManager | TsvDatasetDirectoryManager":
        if storage_variant is StorageVariant.JSON_LINES:
            from dbnomics_data_model.storage.adapters.filesystem.variants.json_lines.json_lines_dataset_directory_manager import (  # noqa: E501
                JsonLinesDatasetDirectoryManager,
            )

            return JsonLinesDatasetDirectoryManager(
                dataset_dir=dataset_dir,
                dataset_id=dataset_id,
                git_provider_directory_manager=git_provider_directory_manager,
                revision_id=revision_id,
                series_offset_repo=series_offset_repo,
            )

        if storage_variant is StorageVariant.TSV:
            from dbnomics_data_model.storage.adapters.filesystem.variants.tsv.tsv_dataset_directory_manager import (
                TsvDatasetDirectoryManager,
            )

            return TsvDatasetDirectoryManager(
                dataset_dir=dataset_dir,
                dataset_id=dataset_id,
                revision_id=revision_id,
                git_provider_directory_manager=git_provider_directory_manager,
            )

        assert_never(storage_variant)

    if revision_id is None:
        if not dataset_dir.is_dir():
            raise DatasetDirectoryNotFound(dataset_dir=dataset_dir, dataset_id=dataset_id)
    else:
        if git_provider_directory_manager is None:
            raise RevisionsNotAvailable
        if not git_provider_directory_manager.has_dir(dataset_dir, revision_id=revision_id):
            raise DatasetDirectoryNotFound(dataset_dir=dataset_dir, dataset_id=dataset_id)

    other_storage_variants = [variant for variant in StorageVariant if variant != default_storage_variant]
    storage_variant_candidates = [default_storage_variant, *other_storage_variants]

    for candidate_storage_variant in storage_variant_candidates:
        dataset_directory_manager = create_for_storage_variant(candidate_storage_variant)
        if dataset_directory_manager.matches_variant(revision_id=revision_id):
            return dataset_directory_manager

    return create_for_storage_variant(default_storage_variant)
