from collections.abc import Iterator

import daiquiri

from dbnomics_data_model.errors import DataModelError
from dbnomics_data_model.model import ProviderCode
from dbnomics_data_model.model.identifiers import DatasetId
from dbnomics_data_model.model.revisions.types import RevisionId
from dbnomics_data_model.storage import Storage
from dbnomics_data_model.storage.errors.category_tree import CategoryTreeStorageError
from dbnomics_data_model.storage.errors.dataset_releases import DatasetReleasesStorageError
from dbnomics_data_model.storage.errors.provider_metadata import ProviderMetadataStorageError

from .category_tree_validator import CategoryTreeValidator
from .dataset_releases_validator import DatasetReleasesValidator
from .dataset_validator import DatasetValidator

logger = daiquiri.getLogger(__name__)


class ProviderValidator:
    def __init__(
        self,
        *,
        provider_code: ProviderCode,
        revision_id: RevisionId | None = None,
        series_per_dataset_limit: int | None = None,
        storage: Storage,
    ) -> None:
        self.provider_code = provider_code
        self.revision_id = revision_id
        self.series_per_dataset_limit = series_per_dataset_limit
        self._storage = storage

    def iter_errors(self) -> Iterator[DataModelError]:
        provider_code = self.provider_code
        logger.debug("Validating data related to provider...", provider_code=provider_code)

        yield from self.iter_provider_metadata_errors(provider_code)
        yield from self.iter_category_tree_errors(provider_code)
        yield from self.iter_dataset_release_errors(provider_code)
        yield from self.iter_dataset_errors(provider_code)

    def iter_category_tree_errors(self, provider_code: ProviderCode) -> Iterator[DataModelError]:
        logger.debug("Validating category tree of provider...", provider_code=provider_code)

        try:
            category_tree = self._storage.load_category_tree(provider_code, revision_id=self.revision_id)
        except CategoryTreeStorageError as exc:
            yield exc
            return

        if category_tree is None:
            return

        category_tree_validator = CategoryTreeValidator(
            category_tree=category_tree, provider_code=provider_code, storage=self._storage
        )
        yield from category_tree_validator.iter_errors()

    def iter_dataset_errors(self, provider_code: ProviderCode) -> Iterator[DataModelError]:
        logger.debug("Validating datasets of provider...", provider_code=provider_code)

        dataset_count = self._storage.get_dataset_count(provider_code, revision_id=self.revision_id)

        for dataset_index, dataset_code in enumerate(
            sorted(self._storage.iter_dataset_codes(provider_code, revision_id=self.revision_id)),
            start=1,
        ):
            dataset_id = DatasetId(provider_code, dataset_code)
            logger.debug("Validating dataset (%d/%d)...", dataset_index, dataset_count, dataset_id=str(dataset_id))
            dataset_validator = DatasetValidator(
                dataset_id=dataset_id,
                revision_id=self.revision_id,
                series_per_dataset_limit=self.series_per_dataset_limit,
                storage=self._storage,
            )
            yield from dataset_validator.iter_errors()

    def iter_dataset_release_errors(self, provider_code: ProviderCode) -> Iterator[DataModelError]:
        logger.debug("Validating releases of datasets of provider...", provider_code=provider_code)

        try:
            dataset_releases_list = list(
                self._storage.iter_dataset_releases(provider_code, revision_id=self.revision_id)
            )
        except DatasetReleasesStorageError as exc:
            yield exc
            return

        for dataset_releases in dataset_releases_list:
            dataset_releases_validator = DatasetReleasesValidator(
                dataset_releases=dataset_releases, provider_code=provider_code, storage=self._storage
            )
            yield from dataset_releases_validator.iter_errors()

    def iter_provider_metadata_errors(self, provider_code: ProviderCode) -> Iterator[DataModelError]:
        logger.debug("Validating provider metadata...", provider_code=provider_code)

        try:
            self._storage.load_provider_metadata(provider_code, revision_id=self.revision_id)
        except ProviderMetadataStorageError as exc:
            yield exc
