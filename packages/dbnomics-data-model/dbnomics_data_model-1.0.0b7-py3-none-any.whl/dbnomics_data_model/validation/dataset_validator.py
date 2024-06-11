from collections import Counter, defaultdict
from collections.abc import Generator, Iterator
from typing import TYPE_CHECKING

import daiquiri
from more_itertools import take

from dbnomics_data_model.errors import DataModelError
from dbnomics_data_model.model import DatasetId, Series
from dbnomics_data_model.model.dataset_metadata import DatasetMetadata
from dbnomics_data_model.model.revisions.types import RevisionId
from dbnomics_data_model.storage import Storage
from dbnomics_data_model.storage.errors.dataset_metadata import DatasetMetadataStorageError
from dbnomics_data_model.validation.validation_settings import overridden_validation_settings

from .errors.dataset_validator import DuplicateSeriesCode, DuplicateSeriesName
from .series_validator import SeriesValidator

if TYPE_CHECKING:
    from collections.abc import Iterable

    from dbnomics_data_model.model import SeriesCode


logger = daiquiri.getLogger(__name__)


class DatasetValidator:
    def __init__(
        self,
        *,
        dataset_id: DatasetId,
        revision_id: RevisionId | None = None,
        series_per_dataset_limit: int | None = None,
        storage: Storage,
    ) -> None:
        self.dataset_id = dataset_id
        self.revision_id = revision_id
        self.series_per_dataset_limit = series_per_dataset_limit
        self._storage = storage

    def iter_errors(self) -> Iterator[DataModelError]:
        dataset_metadata = yield from self.iter_dataset_metadata_errors()
        self.iter_series_errors(dataset_metadata=dataset_metadata)

    def iter_dataset_metadata_errors(self) -> Generator[DataModelError, None, DatasetMetadata | None]:
        dataset_id = self.dataset_id
        logger.debug("Validating dataset metadata...", dataset_id=str(dataset_id))

        try:
            return self._storage.load_dataset_metadata(dataset_id, revision_id=self.revision_id)
        except DatasetMetadataStorageError as exc:
            yield exc

        return None

    def iter_series_errors(self, *, dataset_metadata: DatasetMetadata | None) -> Iterator[DataModelError]:
        """Validate each series of a dataset.

        Validate also that they all have a unique code (and name if defined).
        """
        dataset_id = self.dataset_id

        logger.debug("Validating series of dataset...", dataset_id=str(dataset_id))

        seen_series_codes: Counter[SeriesCode] = Counter()
        seen_series_names: defaultdict[str, set[SeriesCode]] = defaultdict(set)

        series_iter = self._iter_series()
        while True:
            try:
                series = next(series_iter)
            except StopIteration:
                break
            except DataModelError as exc:
                yield exc
                return

            series_code = series.code
            series_name = series.name

            seen_series_codes[series_code] += 1

            if series_name is not None:
                seen_series_names[series_name].add(series_code)

            dataset_dimensions = dataset_metadata.dimensions if dataset_metadata is not None else None
            series_validator = SeriesValidator(
                dataset_dimensions=dataset_dimensions, dataset_id=dataset_id, series=series
            )
            yield from series_validator.iter_errors()

        for series_code, count in sorted(seen_series_codes.most_common()):
            if count > 1:
                yield DuplicateSeriesCode(count=count, dataset_id=dataset_id, series_code=series_code)

        for series_name, series_codes in sorted(seen_series_names.items()):
            if len(series_codes) > 1:
                yield DuplicateSeriesName(dataset_id=dataset_id, series_name=series_name, series_codes=series_codes)

    def _iter_series(self) -> Iterator[Series]:
        dataset_id = self.dataset_id

        with overridden_validation_settings(disable_series_validation=True):
            series_iter: Iterable[Series] = self._storage.iter_dataset_series(dataset_id, revision_id=self.revision_id)

        series_limit = self.series_per_dataset_limit
        if series_limit is not None:
            logger.debug(
                "Will validate a maximum of %d series for this dataset",
                self.series_per_dataset_limit,
                dataset_id=str(self.dataset_id),
            )
            series_iter = take(series_limit, series_iter)

        yield from series_iter
