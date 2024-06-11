from collections.abc import Iterator

import daiquiri

from dbnomics_data_model.errors import DataModelError
from dbnomics_data_model.model import CategoryTree, DatasetCode, DatasetReference, ProviderCode
from dbnomics_data_model.model.identifiers import DatasetId
from dbnomics_data_model.storage import Storage
from dbnomics_data_model.storage.errors.dataset_metadata import DatasetMetadataLoadError

from .errors.category_tree_validator import DanglingCategoryTreeDatasetReference, DatasetMissingFromCategoryTree

logger = daiquiri.getLogger(__name__)


class CategoryTreeValidator:
    def __init__(self, *, category_tree: CategoryTree, provider_code: ProviderCode, storage: Storage) -> None:
        self.category_tree = category_tree
        self.provider_code = provider_code
        self._storage = storage

    def iter_errors(self) -> Iterator[DataModelError]:
        """Check that the datasets referenced by the category tree actually exist in storage.

        Check that the datasets of storage are referenced by the category tree, except for discontinued datasets.
        """
        provider_code = self.provider_code

        storage_dataset_codes = set(self._storage.iter_dataset_codes(provider_code))
        category_tree_dataset_references = list(self.category_tree.iter_dataset_references())

        yield from self.iter_dataset_reference_errors(storage_dataset_codes, category_tree_dataset_references)
        yield from self.iter_stored_datasets_errors(storage_dataset_codes, category_tree_dataset_references)

    def iter_dataset_reference_errors(
        self, storage_dataset_codes: set[DatasetCode], category_tree_dataset_references: list[DatasetReference]
    ) -> Iterator[DataModelError]:
        for dataset_reference in category_tree_dataset_references:
            if dataset_reference.code in storage_dataset_codes:
                continue

            dataset_id = DatasetId(self.provider_code, dataset_reference.code)
            yield DanglingCategoryTreeDatasetReference(dataset_id=dataset_id)

    def iter_stored_datasets_errors(
        self, storage_dataset_codes: set[DatasetCode], category_tree_dataset_references: list[DatasetReference]
    ) -> Iterator[DataModelError]:
        category_tree_dataset_codes = {dataset_reference.code for dataset_reference in category_tree_dataset_references}
        for dataset_code in storage_dataset_codes:
            if dataset_code in category_tree_dataset_codes:
                continue

            dataset_id = DatasetId(self.provider_code, dataset_code)

            try:
                dataset_metadata = self._storage.load_dataset_metadata(dataset_id)
            except DatasetMetadataLoadError:
                logger.exception(
                    "Could not load dataset metadata to see if it's discontinued, considering it's not",
                    dataset_code=dataset_code,
                )
            else:
                # Ignore discontinued dataset because they are allowed be absent from category tree.
                if dataset_metadata.discontinued:
                    continue

            yield DatasetMissingFromCategoryTree(dataset_id)
