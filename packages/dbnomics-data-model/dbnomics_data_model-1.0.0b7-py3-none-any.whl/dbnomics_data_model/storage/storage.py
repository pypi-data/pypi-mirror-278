from abc import ABC, abstractmethod
from collections.abc import Iterable, Iterator
from typing import TYPE_CHECKING

from more_itertools import ilen

from dbnomics_data_model.diff_utils.data_patch import DataPatch
from dbnomics_data_model.model import (
    BareDatasetId,
    CategoryTree,
    DatasetCode,
    DatasetId,
    DatasetMetadata,
    DatasetReleases,
    ProviderCode,
    ProviderMetadata,
    ResolvableDatasetId,
    Series,
    SeriesCode,
    SeriesId,
)
from dbnomics_data_model.model.constants import LATEST_RELEASE
from dbnomics_data_model.model.errors.dataset_releases import DatasetHasNoRelease
from dbnomics_data_model.model.revisions.revision import Revision
from dbnomics_data_model.model.revisions.types import RevisionId
from dbnomics_data_model.storage.errors.storage_uri import UnsupportedStorageUriScheme
from dbnomics_data_model.utils import find

if TYPE_CHECKING:
    from dbnomics_data_model.storage import StorageSession
    from dbnomics_data_model.storage.storage_uri import StorageUri

__all__ = ["Storage"]


class Storage(ABC):
    """A storage contains data for a specific provider."""

    @classmethod
    def from_uri(cls, uri: "StorageUri") -> "Storage":
        from dbnomics_data_model.storage.adapters.filesystem.file_system_storage_uri import FileSystemStorageUri

        if isinstance(uri, FileSystemStorageUri):
            from dbnomics_data_model.storage.adapters.filesystem.file_system_storage import FileSystemStorage

            return FileSystemStorage.from_uri(uri)

        raise UnsupportedStorageUriScheme(scheme=uri.scheme)

    @abstractmethod
    def create_session(self, name: str) -> "StorageSession":
        pass

    def dataset_has_any_series(self, dataset_id: DatasetId) -> bool:
        """Return True if the dataset has series."""
        first_series = next(self.iter_dataset_series(dataset_id, with_observations=False), None)
        return first_series is not None

    @abstractmethod
    def delete_category_tree(self, provider_code: ProviderCode, *, missing_ok: bool = False) -> None:
        """Delete the category tree of a provider."""

    @abstractmethod
    def delete_dataset(self, dataset_id: DatasetId, *, missing_ok: bool = False) -> None:
        """Delete data related to a dataset."""

    @abstractmethod
    def delete_dataset_metadata(self, dataset_id: DatasetId, *, missing_ok: bool = False) -> None:
        """Delete dataset metadata."""

    @abstractmethod
    def delete_dataset_releases(self, provider_code: ProviderCode, *, missing_ok: bool = False) -> None:
        """Delete dataset releases of a provider."""

    @abstractmethod
    def delete_dataset_series(self, dataset_id: DatasetId, *, missing_ok: bool = False) -> None:
        """Delete the series of a dataset."""

    @abstractmethod
    def delete_provider(self, provider_code: ProviderCode, *, missing_ok: bool = False) -> None:
        """Delete data related to a provider."""

    @abstractmethod
    def delete_provider_metadata(self, provider_code: ProviderCode, *, missing_ok: bool = False) -> None:
        """Delete provider metadata."""

    def get_dataset_count(self, provider_code: ProviderCode, *, revision_id: RevisionId | None = None) -> int:
        """Return the number of datasets for a provider."""
        return ilen(self.iter_dataset_codes(provider_code, revision_id=revision_id))

    def get_provider_count(self, *, revision_id: RevisionId | None = None) -> int:
        """Return the number of providers."""
        return ilen(self.iter_provider_codes(revision_id=revision_id))

    @abstractmethod
    def has_dataset(self, dataset_id: DatasetId, *, revision_id: RevisionId | None = None) -> bool:
        """Return True if dataset exists."""

    @abstractmethod
    def has_dataset_metadata(self, dataset_id: DatasetId, *, revision_id: RevisionId | None = None) -> bool:
        """Return True if dataset metadata exists."""

    @abstractmethod
    def has_series(self, series_id: SeriesId, *, revision_id: RevisionId | None = None) -> bool:
        """Return True if the series exists."""

    @abstractmethod
    def iter_dataset_codes(
        self, provider_code: ProviderCode, *, revision_id: RevisionId | None = None
    ) -> Iterator[DatasetCode]:
        """Yield the code of each dataset of a provider."""

    @abstractmethod
    def iter_dataset_releases(
        self, provider_code: ProviderCode, *, revision_id: RevisionId | None = None
    ) -> Iterator[DatasetReleases]:
        """Yield releases of datasets sharing the same bare dataset code."""

    @abstractmethod
    def iter_dataset_series(
        self,
        dataset_id: DatasetId,
        *,
        revision_id: RevisionId | None = None,
        series_codes: Iterable[SeriesCode] | None = None,
        with_observations: bool = True,
    ) -> Iterator[Series]:
        """Yield series of the given dataset.

        Observations are included by default in yielded series, but can be excluded.

        Series can be filtered by code by using `series_codes`.
        Note: yielded series are not guaranteed to follow the order of `series_codes`.
        """

    @abstractmethod
    def iter_provider_codes(self, *, revision_id: RevisionId | None = None) -> Iterator[ProviderCode]:
        """Yield the code of each provider."""

    # TODO add iter_changes (whole DB), iter_dataset_changes, iter_dataset_metadata_changes, iter_provider_changes, iter_provider_metadata_changes, iter_category_tree_changes

    @abstractmethod
    def iter_series_changes(
        self, series_id: SeriesId, *, start_revision_id: RevisionId | None = None
    ) -> Iterator[tuple[Revision, DataPatch]]:
        """Yield series revisions, most recent first."""

    @abstractmethod
    def load_category_tree(
        self, provider_code: ProviderCode, *, revision_id: RevisionId | None = None
    ) -> CategoryTree | None:
        """Return the category tree of a provider.

        If not found return None because category tree is optional.
        """

    @abstractmethod
    def load_dataset_metadata(self, dataset_id: DatasetId, *, revision_id: RevisionId | None = None) -> DatasetMetadata:
        """Load dataset metadata."""

    def load_dataset_releases(
        self, bare_dataset_id: BareDatasetId, *, revision_id: RevisionId | None = None
    ) -> DatasetReleases | None:
        """Return the releases of a dataset sharing the same bare dataset code.

        If not found return None because dataset releases are optional.
        """
        return find(
            lambda dataset_releases: dataset_releases.bare_dataset_code == bare_dataset_id.bare_dataset_code,
            self.iter_dataset_releases(bare_dataset_id.provider_code, revision_id=revision_id),
        )

    @abstractmethod
    def load_provider_metadata(
        self, provider_code: ProviderCode, *, revision_id: RevisionId | None = None
    ) -> ProviderMetadata:
        """Load provider metadata."""

    @abstractmethod
    def load_series(
        self, series_id: SeriesId, *, revision_id: RevisionId | None = None, with_observations: bool = True
    ) -> Series:
        """Load a series.

        Observations are included by default in yielded series, but can be excluded.
        """

    def resolve_dataset_code(
        self, resolvable_dataset_id: ResolvableDatasetId, *, revision_id: RevisionId | None = None
    ) -> DatasetId:
        resolvable_dataset_code = resolvable_dataset_id.resolvable_dataset_code
        bare_dataset_code = resolvable_dataset_code.bare_dataset_code
        resolvable_release_code = resolvable_dataset_code.resolvable_release_code
        if resolvable_release_code is None or resolvable_release_code != LATEST_RELEASE:
            dataset_code = DatasetCode(bare_dataset_code, release_code=resolvable_release_code)
            return DatasetId(resolvable_dataset_id.provider_code, dataset_code)

        bare_dataset_id = BareDatasetId(resolvable_dataset_id.provider_code, bare_dataset_code)

        dataset_releases = self.load_dataset_releases(bare_dataset_id, revision_id=revision_id)

        if dataset_releases is None:
            raise DatasetHasNoRelease(bare_dataset_id)

        release_code = dataset_releases.resolve_release_code(resolvable_release_code)
        dataset_code = DatasetCode(bare_dataset_code, release_code=release_code)
        return DatasetId(resolvable_dataset_id.provider_code, dataset_code)

    @abstractmethod
    def save_category_tree(self, category_tree: CategoryTree, *, provider_code: ProviderCode) -> None:
        """Save a category tree of a provider."""

    # TODO remove dimensions that have no values (can't be used by any series anyway)

    @abstractmethod
    def save_dataset_metadata(self, dataset_metadata: DatasetMetadata, *, provider_code: ProviderCode) -> None:
        """Save dataset metadata."""

    @abstractmethod
    def save_dataset_releases(
        self, dataset_releases: DatasetReleases | Iterable[DatasetReleases], *, provider_code: ProviderCode
    ) -> None:
        """Save the releases of a dataset sharing the same bare dataset code."""

    @abstractmethod
    def save_series(self, series: Series | Iterable[Series], *, dataset_id: DatasetId) -> None:
        """Save series of a dataset."""

    @abstractmethod
    def save_provider_metadata(self, provider_metadata: ProviderMetadata) -> None:
        """Save provider metadata."""
