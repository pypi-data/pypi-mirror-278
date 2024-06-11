from typing import assert_never

import daiquiri

from dbnomics_data_model.model import DatasetId, ProviderCode
from dbnomics_data_model.model.merge_utils import iter_merged_items
from dbnomics_data_model.storage import Storage, UpdateStrategy
from dbnomics_data_model.storage.errors.provider_metadata import ProviderMetadataNotFound

logger = daiquiri.getLogger(__name__)


class StorageUpdater:
    def __init__(self, *, source_storage: Storage, target_storage: Storage) -> None:
        self.source_storage = source_storage
        self.target_storage = target_storage

    def merge_category_tree(self, provider_code: ProviderCode) -> None:
        source_category_tree = self.source_storage.load_category_tree(provider_code)
        if source_category_tree is None:
            return

        target_category_tree = self.target_storage.load_category_tree(provider_code)
        if target_category_tree is None:
            self.target_storage.save_category_tree(source_category_tree, provider_code=provider_code)
            return

        merged_category_tree = target_category_tree.merge(source_category_tree)
        self.target_storage.save_category_tree(merged_category_tree, provider_code=provider_code)

    def merge_dataset(self, dataset_id: DatasetId) -> None:
        """Merge the given dataset of target storage with the one of source storage.

        Merge dataset metadata, then merge all series (metadata and observations).
        """
        if not self.source_storage.has_dataset(dataset_id):
            return

        if not self.target_storage.has_dataset(dataset_id):
            self.replace_dataset(dataset_id)
            return

        # Merge dataset metadata
        target_dataset_metadata = self.target_storage.load_dataset_metadata(dataset_id)
        source_dataset_metadata = self.source_storage.load_dataset_metadata(dataset_id)
        merged_dataset_metadata = target_dataset_metadata.merge(source_dataset_metadata)

        # Merge all series
        target_series_iter = self.target_storage.iter_dataset_series(dataset_id)
        source_series_iter = self.source_storage.iter_dataset_series(dataset_id)
        merged_series_iter = iter_merged_items(
            key=lambda series: series.code,
            merge=lambda source, target: target.merge(source),
            source=source_series_iter,
            target=target_series_iter,
        )

        # Do the save
        self.target_storage.delete_dataset(dataset_id)
        self.target_storage.save_dataset_metadata(merged_dataset_metadata, provider_code=dataset_id.provider_code)
        self.target_storage.save_series(merged_series_iter, dataset_id=dataset_id)

    def merge_dataset_releases(self, provider_code: ProviderCode) -> None:
        source_dataset_releases_list = list(self.source_storage.iter_dataset_releases(provider_code))
        if not source_dataset_releases_list:
            return

        target_dataset_releases_list = list(self.target_storage.iter_dataset_releases(provider_code))
        merged_dataset_releases_list = iter_merged_items(
            key=lambda dataset_releases: dataset_releases.bare_dataset_code,
            merge=lambda source, target: target.merge(source),
            source=source_dataset_releases_list,
            target=target_dataset_releases_list,
        )

        for merged_dataset_releases in merged_dataset_releases_list:
            self.target_storage.save_dataset_releases(merged_dataset_releases, provider_code=provider_code)

    def replace_category_tree(self, provider_code: ProviderCode) -> None:
        source_category_tree = self.source_storage.load_category_tree(provider_code)
        if source_category_tree is None:
            return

        self.target_storage.save_category_tree(source_category_tree, provider_code=provider_code)

    def replace_dataset(self, dataset_id: DatasetId) -> None:
        source_dataset_metadata = self.source_storage.load_dataset_metadata(dataset_id)
        source_series_iter = self.source_storage.iter_dataset_series(dataset_id)

        self.target_storage.delete_dataset(dataset_id, missing_ok=True)
        self.target_storage.save_dataset_metadata(source_dataset_metadata, provider_code=dataset_id.provider_code)
        self.target_storage.save_series(source_series_iter, dataset_id=dataset_id)

    def replace_provider_metadata(self, provider_code: ProviderCode, *, missing_ok: bool = False) -> None:
        logger.info(
            "Replacing provider metadata of %r with the one of %r",
            self.target_storage,
            self.source_storage,
            provider_code=provider_code,
        )
        try:
            source_provider_metadata = self.source_storage.load_provider_metadata(provider_code)
        except ProviderMetadataNotFound:
            if missing_ok:
                return
            raise

        self.target_storage.save_provider_metadata(source_provider_metadata)

    def update(
        self,
        *,
        category_tree_update_strategy: UpdateStrategy | None = None,
        dataset_update_strategy: UpdateStrategy | None = None,
    ) -> None:
        logger.info("Updating data of %r with equivalent data of %r", self.target_storage, self.source_storage)
        for provider_code in self.source_storage.iter_provider_codes():
            self.update_provider(
                provider_code,
                category_tree_update_strategy=category_tree_update_strategy,
                dataset_update_strategy=dataset_update_strategy,
            )

    def update_category_tree(
        self, provider_code: ProviderCode, *, update_strategy: UpdateStrategy | None = None
    ) -> None:
        if update_strategy is None:
            update_strategy = UpdateStrategy.MERGE

        logger.info(
            "Updating category tree of %r with the one of %r",
            self.target_storage,
            self.source_storage,
            provider_code=provider_code,
            update_strategy=update_strategy,
        )

        if update_strategy is UpdateStrategy.REPLACE:
            self.replace_category_tree(provider_code)
        elif update_strategy is UpdateStrategy.MERGE:
            self.merge_category_tree(provider_code)
        else:
            assert_never(update_strategy)

    def update_dataset(self, dataset_id: DatasetId, *, update_strategy: UpdateStrategy | None = None) -> None:
        """Update the given dataset of target storage with the same one in source storage.

        The update strategy can be "replace" (default) or "merge".

        With the "replace" strategy, dataset metadata and series are replaced by the source dataset.

        With the "merge" strategy, dataset metadata and series are merged with the source dataset.
        """
        if update_strategy is None:
            update_strategy = UpdateStrategy.REPLACE

        logger.info(
            "Updating dataset %r of %r with the one of %r",
            str(dataset_id),
            self.target_storage,
            self.source_storage,
            update_strategy=update_strategy,
        )

        if update_strategy is UpdateStrategy.REPLACE:
            self.replace_dataset(dataset_id)
        elif update_strategy is UpdateStrategy.MERGE:
            self.merge_dataset(dataset_id)
        else:
            assert_never(update_strategy)

    def update_dataset_releases(
        self, provider_code: ProviderCode, *, update_strategy: UpdateStrategy | None = None
    ) -> None:
        if update_strategy is None:
            update_strategy = UpdateStrategy.MERGE

        logger.info(
            "Updating dataset releases of %r with the one of %r",
            self.target_storage,
            self.source_storage,
            provider_code=provider_code,
            update_strategy=update_strategy,
        )

        if update_strategy is UpdateStrategy.MERGE:
            self.merge_dataset_releases(provider_code)
        else:
            msg = f"update_strategy={update_strategy!r} is not implemented for dataset release metadata"
            raise NotImplementedError(msg)

    def update_provider(
        self,
        provider_code: ProviderCode,
        *,
        category_tree_update_strategy: UpdateStrategy | None = None,
        dataset_update_strategy: UpdateStrategy | None = None,
    ) -> None:
        logger.info(
            "Updating data related to provider of %r with equivalent data of %r",
            self.target_storage,
            self.source_storage,
            provider_code=provider_code,
        )
        self.replace_provider_metadata(provider_code, missing_ok=True)
        self.update_category_tree(provider_code, update_strategy=category_tree_update_strategy)
        self.update_dataset_releases(provider_code)
        self.update_provider_datasets(provider_code, update_strategy=dataset_update_strategy)

    def update_provider_datasets(
        self, provider_code: ProviderCode, *, update_strategy: UpdateStrategy | None = None
    ) -> None:
        for source_dataset_code in self.source_storage.iter_dataset_codes(provider_code):
            dataset_id = DatasetId(provider_code, source_dataset_code)
            self.update_dataset(dataset_id, update_strategy=update_strategy)
