from collections.abc import Iterable, Iterator
from contextlib import AbstractContextManager, nullcontext
from pathlib import Path
from typing import Final

import daiquiri

from dbnomics_data_model.errors import DataModelError
from dbnomics_data_model.model import DatasetMetadata, Observation, Series, SeriesCode
from dbnomics_data_model.model.constants import PERIOD, VALUE
from dbnomics_data_model.model.identifiers import SeriesId
from dbnomics_data_model.model.revisions.types import RevisionId, RevisionMetadata
from dbnomics_data_model.storage.adapters.filesystem.base_dataset_directory_manager import BaseDatasetDirectoryManager
from dbnomics_data_model.storage.adapters.filesystem.constants import DATASET_JSON
from dbnomics_data_model.storage.adapters.filesystem.errors.dataset_directory import DatasetDirectoryCreateError
from dbnomics_data_model.storage.adapters.filesystem.errors.dataset_json_file import (
    DatasetJsonLoadError,
    DatasetJsonNotFound,
    DatasetJsonSaveError,
)
from dbnomics_data_model.storage.adapters.filesystem.storage_variant import StorageVariant
from dbnomics_data_model.storage.adapters.filesystem.variants.tsv.errors.series_tsv_file import (
    SeriesTsvDeleteError,
    SeriesTsvLoadError,
    SeriesTsvNotFound,
    SeriesTsvSaveError,
)
from dbnomics_data_model.storage.errors.dataset import (
    DatasetHasNoSeries,
    DatasetSeriesLoadError,
    DatasetSomeSeriesDeleteError,
    DatasetSomeSeriesSaveError,
)
from dbnomics_data_model.storage.errors.dataset_metadata import DatasetMetadataSaveError
from dbnomics_data_model.storage.errors.revisions import LatestRevisionOnlyOperation, RevisionsNotAvailable
from dbnomics_data_model.storage.errors.series import SeriesLoadError, SeriesNotFound

from .errors.tsv_utils import InvalidTsvObservationHeader, TsvError
from .model.tsv_dataset_json import TsvDatasetJson
from .model.tsv_series_json import TsvSeriesJson
from .tsv_utils import iter_tsv_rows, iter_tsv_text_rows, save_tsv_file

__all__ = ["TsvDatasetDirectoryManager"]


logger = daiquiri.getLogger(__name__)

TSV_SUFFIX: Final = "tsv"


class TsvDatasetDirectoryManager(BaseDatasetDirectoryManager[TsvDatasetJson]):
    @property
    def dataset_json_class(self) -> type[TsvDatasetJson]:
        return TsvDatasetJson

    def delete_dataset_metadata(self, *, missing_ok: bool = False) -> None:  # noqa: ARG002
        msg = "Can't delete dataset metadata in TSV dataset variant because dataset.json contains also series metadata."
        raise NotImplementedError(msg)

    def delete_series(self, *, missing_ok: bool = False) -> None:
        if self.revision_id is not None:
            raise LatestRevisionOnlyOperation(revision_id=self.revision_id)

        try:
            self.delete_series_metadata_from_dataset_json()
        except (DatasetJsonLoadError, DatasetJsonSaveError) as exc:
            raise DatasetSomeSeriesDeleteError(dataset_id=self.dataset_id) from exc

        try:
            self.delete_series_tsv_files(missing_ok=missing_ok)
        except SeriesTsvDeleteError as exc:
            raise DatasetSomeSeriesDeleteError(dataset_id=self.dataset_id) from exc

    def delete_series_metadata_from_dataset_json(self) -> None:
        if self.revision_id is not None:
            raise LatestRevisionOnlyOperation(revision_id=self.revision_id)

        try:
            dataset_json = self.load_dataset_json()
        except DatasetJsonNotFound:
            return

        if not dataset_json.series:
            return

        dataset_json.series = []

        self.save_dataset_json(dataset_json)

    def delete_series_tsv_files(self, *, missing_ok: bool = False) -> None:
        if self.revision_id is not None:
            raise LatestRevisionOnlyOperation(revision_id=self.revision_id)

        tsv_files = list(self.iter_series_tsv_files())
        if not tsv_files and not missing_ok:
            raise DatasetHasNoSeries(dataset_id=self.dataset_id)

        for series_tsv_path in tsv_files:
            try:
                series_tsv_path.unlink()
            except Exception as exc:
                raise SeriesTsvDeleteError(dataset_id=self.dataset_id, series_tsv_path=series_tsv_path) from exc

    def get_revision_metadata_for_series(self, series_code: SeriesCode) -> RevisionMetadata:
        return {"file": self.get_series_tsv_path(series_code)}

    def get_series_tsv_path(self, series_code: SeriesCode) -> Path:
        return self.dataset_dir / self.get_series_tsv_file_name(series_code)

    def get_series_tsv_file_name(self, series_code: SeriesCode) -> str:
        return f"{series_code}.{TSV_SUFFIX}"

    def has_series(self, series_code: SeriesCode) -> bool:
        # Optimize method of parent class by just checking that the TSV file exists instead of loading the series.

        if self.revision_id is None:
            series_tsv_path = self.get_series_tsv_path(series_code)
            return series_tsv_path.is_file()

        if self._git_provider_directory_manager is None:
            raise RevisionsNotAvailable

        return self._git_provider_directory_manager.has_file(series_tsv_path, revision_id=self.revision_id)

    def iter_observations(self, series_code: SeriesCode) -> Iterator[Observation]:
        with self._get_series_line_iter_context_manager(series_code) as line_iter:
            try:
                yield from self.iter_tsv_observations(line_iter, series_code=series_code)
            except TsvError as exc:
                series_tsv_path = self.get_series_tsv_path(series_code)
                raise SeriesTsvLoadError(
                    dataset_id=self.dataset_id,
                    revision_id=self.revision_id,
                    series_code=series_code,
                    series_tsv_path=series_tsv_path,
                ) from exc

    def iter_series(
        self, *, series_codes: Iterable[SeriesCode] | None = None, with_observations: bool = True
    ) -> Iterator[Series]:
        """Yield Series objects from a dataset stored using TSV variant.

        Start by reading series metadata in `dataset.json` `series` property,
        and for each one read the corresponding TSV file for observations.
        """
        series_codes_list = None if series_codes is None else list(series_codes)

        dataset_json = self.load_dataset_json()
        dataset_metadata = dataset_json.to_domain_model()

        yielded_line_codes: set[str] = set()
        series_codes_set = None if series_codes_list is None else set(series_codes_list)

        for series_json in dataset_json.series:
            if series_codes_list is not None and series_json.code not in series_codes_list:
                continue

            try:
                series = series_json.to_domain_model(dataset_dimensions=dataset_metadata.dimensions)
            except DataModelError as exc:
                raise DatasetSeriesLoadError(
                    dataset_id=self.dataset_id, revision_id=self.revision_id, series_code=series_json.code
                ) from exc

            if with_observations:
                series_id = SeriesId.from_dataset_id(self.dataset_id, series.code)
                try:
                    series.observations = list(self.iter_observations(series.code))
                except SeriesTsvNotFound as exc:
                    raise SeriesNotFound(revision_id=self.revision_id, series_id=series_id) from exc
                except SeriesTsvLoadError as exc:
                    raise SeriesLoadError(revision_id=self.revision_id, series_id=series_id) from exc

            yield series
            yielded_line_codes.add(series.code)

            if series_codes_set is not None and yielded_line_codes == series_codes_set:
                break

    def iter_series_tsv_files(self) -> Iterator[Path]:
        yield from self.dataset_dir.glob(f"*.{TSV_SUFFIX}")

    def iter_tsv_observations(self, lines: Iterator[str], *, series_code: SeriesCode) -> Iterator[Observation]:
        """Yield Observation model entities from TSV file."""
        header_min_length: Final = 2

        text_rows = iter_tsv_text_rows(lines)
        try:
            header = next(text_rows)
        except StopIteration:
            return

        if len(header) < header_min_length or header[0] != PERIOD or header[1] != VALUE:
            series_id = SeriesId.from_dataset_id(self.dataset_id, series_code)
            series_tsv_path = self.get_series_tsv_path(series_code)
            raise InvalidTsvObservationHeader(header=header, series_id=series_id, series_tsv_path=series_tsv_path)

        attribute_codes = header[2:]

        for (period, value), attribute_value_codes in iter_tsv_rows(text_rows):
            attributes = {
                attribute_code: attribute_value_code
                for attribute_code, attribute_value_code in zip(attribute_codes, attribute_value_codes, strict=True)
                if attribute_value_code
            }
            yield Observation.create(attributes=attributes, period=period, value=value)

    def matches_variant(self, *, revision_id: RevisionId | None = None) -> bool:
        if revision_id is None:
            return any(self.iter_series_tsv_files())

        if self._git_provider_directory_manager is None:
            raise RevisionsNotAvailable

        return any(
            self._git_provider_directory_manager.iter_blobs_matching_name(
                lambda path: path.suffix == f".{TSV_SUFFIX}", revision_id=revision_id, sub_tree=str(self.dataset_code)
            )
        )

    def save_dataset_metadata(self, dataset_metadata: DatasetMetadata) -> None:
        if self.revision_id is not None:
            raise LatestRevisionOnlyOperation(revision_id=self.revision_id)

        self._validate_dataset_metadata_code_matches(dataset_metadata)

        dataset_json = TsvDatasetJson.from_domain_model(dataset_metadata)

        # Keep existing series metadata from dataset.json
        try:
            existing_dataset_json = self.load_dataset_json()
        except DatasetJsonNotFound:
            pass
        else:
            dataset_json.series = existing_dataset_json.series

        try:
            self.save_dataset_json(dataset_json)
        except (DatasetDirectoryCreateError, DatasetJsonSaveError) as exc:
            raise DatasetMetadataSaveError(dataset_id=self.dataset_id, dataset_metadata=dataset_metadata) from exc

    def save_series(self, series: Series | Iterable[Series]) -> None:
        if self.revision_id is not None:
            raise LatestRevisionOnlyOperation(revision_id=self.revision_id)

        # TODO track known series codes to ensure no duplicates are added

        try:
            dataset_json = self.load_dataset_json()
        except DatasetJsonNotFound as exc:
            logger.exception(
                "With TSV variant, series metadata is embedded in %s, but the file doesn't exist yet. Hint: save dataset metadata before any series.",  # noqa: E501
                DATASET_JSON,
            )
            raise DatasetSomeSeriesSaveError(dataset_id=self.dataset_id) from exc

        series_iter = [series] if isinstance(series, Series) else series

        for series in series_iter:
            # Append series metadata to dataset.json
            series_json = TsvSeriesJson.from_domain_model(series)
            dataset_json.series.append(series_json)

            # Save series observations
            try:
                self.save_series_tsv(series)
            except SeriesTsvSaveError as exc:
                raise DatasetSomeSeriesSaveError(dataset_id=self.dataset_id) from exc

        # Save series metadata via updated dataset.json
        try:
            self.save_dataset_json(dataset_json)
        except DatasetJsonSaveError as exc:
            raise DatasetSomeSeriesSaveError(dataset_id=self.dataset_id) from exc

    def save_series_tsv(self, series: Series) -> None:
        if self.revision_id is not None:
            raise LatestRevisionOnlyOperation(revision_id=self.revision_id)

        if not series.observations:
            return

        series_tsv_path = self.get_series_tsv_path(series.code)

        try:
            save_tsv_file(series_tsv_path, series)
        except TsvError as exc:
            raise SeriesTsvSaveError(
                dataset_id=self.dataset_id, series_code=series.code, series_tsv_path=series_tsv_path
            ) from exc

    @property
    def storage_variant(self) -> StorageVariant:
        return StorageVariant.TSV

    def _get_series_line_iter_context_manager(self, series_code: SeriesCode) -> AbstractContextManager[Iterator[str]]:
        series_tsv_path = self.get_series_tsv_path(series_code)

        if self.revision_id is None:
            try:
                return series_tsv_path.open("rt", encoding="utf-8")
            except FileNotFoundError as exc:
                raise SeriesTsvNotFound(
                    dataset_id=self.dataset_id, series_code=series_code, series_tsv_path=series_tsv_path
                ) from exc

        if self._git_provider_directory_manager is None:
            raise RevisionsNotAvailable

        series_tsv_blob = self._git_provider_directory_manager.load_blob(series_tsv_path, revision_id=self.revision_id)
        line_iter = (line.decode("utf-8") for line in series_tsv_blob.data_stream.stream)
        return nullcontext(line_iter)
