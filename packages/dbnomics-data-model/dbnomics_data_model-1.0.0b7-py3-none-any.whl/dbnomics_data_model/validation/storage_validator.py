from collections.abc import Iterator

import daiquiri

from dbnomics_data_model.errors import DataModelError
from dbnomics_data_model.model import ProviderCode
from dbnomics_data_model.model.revisions.types import RevisionId
from dbnomics_data_model.storage import Storage

from .provider_validator import ProviderValidator

logger = daiquiri.getLogger(__name__)


class StorageValidator:
    def __init__(
        self,
        *,
        revision_id: RevisionId | None = None,
        series_per_dataset_limit: int | None = None,
        storage: Storage,
    ) -> None:
        self.revision_id = revision_id
        self.series_per_dataset_limit = series_per_dataset_limit
        self._storage = storage

    def iter_errors(self) -> Iterator[DataModelError]:
        logger.debug("Validating storage...", storage=self._storage)

        for provider_code in self._storage.iter_provider_codes():
            yield from self.iter_provider_errors(provider_code)

    def iter_provider_errors(self, provider_code: ProviderCode) -> Iterator[DataModelError]:
        provider_validator = ProviderValidator(
            provider_code=provider_code,
            revision_id=self.revision_id,
            series_per_dataset_limit=self.series_per_dataset_limit,
            storage=self._storage,
        )
        yield from provider_validator.iter_errors()
