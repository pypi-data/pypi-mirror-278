from collections.abc import Iterator

import daiquiri

from dbnomics_data_model.errors import DataModelError
from dbnomics_data_model.model import DatasetCode, DatasetReleases, ProviderCode
from dbnomics_data_model.model.identifiers import DatasetId
from dbnomics_data_model.storage import Storage

from .errors.dataset_releases_validator import DanglingDatasetReleasesDatasetReference

logger = daiquiri.getLogger(__name__)


class DatasetReleasesValidator:
    def __init__(self, *, dataset_releases: DatasetReleases, provider_code: ProviderCode, storage: Storage) -> None:
        self.dataset_releases = dataset_releases
        self.provider_code = provider_code
        self._storage = storage

    def iter_errors(self) -> Iterator[DataModelError]:
        yield from self.iter_dataset_reference_errors()

    def iter_dataset_reference_errors(self) -> Iterator[DataModelError]:
        """Check that the datasets referenced by the releases actually exist in storage."""
        dataset_releases = self.dataset_releases
        provider_code = self.provider_code
        storage_dataset_codes = set(self._storage.iter_dataset_codes(provider_code))

        for release_code in dataset_releases.release_codes:
            dataset_code = DatasetCode(dataset_releases.bare_dataset_code, release_code=release_code)
            if dataset_code not in storage_dataset_codes:
                dataset_id = DatasetId(provider_code, dataset_code)
                yield DanglingDatasetReleasesDatasetReference(dataset_id=dataset_id)
