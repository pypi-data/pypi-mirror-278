from collections.abc import Generator, Iterator
from contextlib import AbstractContextManager, nullcontext
from pathlib import Path
from typing import BinaryIO, cast

import daiquiri

from dbnomics_data_model.errors import DataModelError
from dbnomics_data_model.json_utils import parse_json_bytes_as_object
from dbnomics_data_model.json_utils.errors import JsonLineParseError, JsonParseError
from dbnomics_data_model.model import SeriesCode
from dbnomics_data_model.model.identifiers.dataset_id import DatasetId
from dbnomics_data_model.model.identifiers.series_id import SeriesId
from dbnomics_data_model.model.revisions.types import RevisionId
from dbnomics_data_model.storage.adapters.filesystem.errors.json_model import JsonModelError
from dbnomics_data_model.storage.adapters.filesystem.file_utils import iter_lines_with_offsets
from dbnomics_data_model.storage.adapters.filesystem.git.git_provider_directory_manager import (
    GitProviderDirectoryManager,
)
from dbnomics_data_model.storage.adapters.filesystem.git.tellable_stream import TellableStream
from dbnomics_data_model.storage.adapters.filesystem.variants.json_lines.parsing import parse_json_line_code
from dbnomics_data_model.storage.errors.revisions import RevisionsNotAvailable

from .errors.series_json_lines_file import (
    SeriesJsonDataParseError,
    SeriesJsonLineCodeMismatch,
    SeriesJsonLineParseError,
    SeriesJsonLineReadError,
    SeriesJsonLineSeekError,
    SeriesJsonLinesNotFound,
    SeriesJsonLinesScanError,
    SomeJsonLinesSeriesNotFound,
)
from .model.json_lines_series_item import JsonLinesSeriesItem
from .offsets.repo import JsonLinesSeriesOffsetRepo
from .offsets.types import JsonLinesOffset

__all__ = ["SeriesJsonLinesItemRepo"]


logger = daiquiri.getLogger(__name__)


class SeriesJsonLinesItemRepo:
    def __init__(
        self,
        *,
        dataset_id: DatasetId,
        git_provider_directory_manager: GitProviderDirectoryManager | None = None,
        revision_id: RevisionId | None = None,
        series_jsonl_path: Path,
        series_offset_repo: JsonLinesSeriesOffsetRepo | None = None,
    ) -> None:
        self.dataset_id = dataset_id
        self.revision_id = revision_id
        self.series_jsonl_path = series_jsonl_path

        self._git_provider_directory_manager = git_provider_directory_manager
        self._series_offset_repo = series_offset_repo

    def iter_json_lines_series_items(
        self, *, series_codes: list[SeriesCode] | None = None, with_observations: bool = True
    ) -> Iterator[JsonLinesSeriesItem]:
        remaining_series_codes = series_codes

        if remaining_series_codes and self._series_offset_repo is not None and self.revision_id is None:
            remaining_series_codes = yield from self.iter_json_lines_series_items_by_seeking(
                series_codes=remaining_series_codes, with_observations=with_observations
            )

        if remaining_series_codes is None or remaining_series_codes:
            if remaining_series_codes and self._series_offset_repo is None and self.revision_id is None:
                logger.warning(
                    "About to load %s of the dataset %r by scanning its JSON Lines file. Consider using a series offset repository for better performance.",  # noqa: E501
                    f"{len(remaining_series_codes)} series",
                    str(self.dataset_id),
                )
            items_iter = self.iter_json_lines_series_items_by_scanning(
                series_codes=remaining_series_codes, with_observations=with_observations
            )
            while True:
                try:
                    # Omit the offset
                    json_lines_series_item, _ = next(items_iter)
                except StopIteration as exc:
                    remaining_series_codes = cast(list[SeriesCode], exc.value)
                    break

                yield json_lines_series_item

        if remaining_series_codes:
            raise SomeJsonLinesSeriesNotFound(
                dataset_id=self.dataset_id,
                revision_id=self.revision_id,
                series_codes=sorted(remaining_series_codes),
                series_jsonl_path=self.series_jsonl_path,
            )

    def iter_json_lines_series_items_by_scanning(
        self, *, series_codes: list[SeriesCode] | None, with_observations: bool = True
    ) -> Generator[tuple[JsonLinesSeriesItem, JsonLinesOffset], None, list[SeriesCode]]:
        series_jsonl_path = self.series_jsonl_path

        yielded_line_codes: set[str] = set()
        series_codes_set = None if series_codes is None else set(series_codes)

        with self._get_series_line_iter_context_manager() as line_iter:
            for line_num, (line, offset) in enumerate(iter_lines_with_offsets(line_iter), start=1):
                line_code = parse_json_line_code(line)
                if series_codes_set is not None and line_code not in series_codes_set:
                    continue

                try:
                    json_lines_series_item = self._parse_json_line_series_item(
                        line, with_observations=with_observations
                    )
                except DataModelError as exc:
                    raise SeriesJsonLinesScanError(
                        dataset_id=self.dataset_id,
                        line_num=line_num,
                        revision_id=self.revision_id,
                        series_jsonl_path=series_jsonl_path,
                    ) from exc

                logger.debug(
                    "Loaded series from JSON Lines file by scanning",
                    input_file=series_jsonl_path,
                    dataset_id=str(self.dataset_id),
                    series_code=line_code,
                    line_num=line_num,
                    offset=offset,
                )

                yield json_lines_series_item, offset
                yielded_line_codes.add(line_code)

                if series_codes_set is not None and yielded_line_codes == series_codes_set:
                    break

        remaining_series_codes = (
            [series_code for series_code in series_codes if series_code not in yielded_line_codes]
            if series_codes is not None
            else []
        )
        return remaining_series_codes

    def iter_json_lines_series_items_by_seeking(
        self, *, series_codes: list[SeriesCode], with_observations: bool = True
    ) -> Generator[JsonLinesSeriesItem, None, list[SeriesCode]]:
        series_offset_repo = self._series_offset_repo
        if series_offset_repo is None:
            msg = f"Can't seek because {type(self).__name__} was initialized with series_offset_repo=None"
            raise RuntimeError(msg)

        series_jsonl_path = self.series_jsonl_path

        series_ids = [SeriesId.from_dataset_id(self.dataset_id, series_code) for series_code in series_codes]
        offsets_iter = series_offset_repo.iter_series_offsets(series_ids)

        yielded_series_codes: set[SeriesCode] = set()

        with series_jsonl_path.open("rb") as fp:
            for series_id, offset in sorted(offsets_iter, key=lambda item: item[1]):
                json_lines_series_item, loaded_series_code = self._load_json_lines_series_by_seeking(
                    fp,
                    offset=offset,
                    series_id=series_id,
                    series_jsonl_path=series_jsonl_path,
                    with_observations=with_observations,
                )
                yield json_lines_series_item
                yielded_series_codes.add(loaded_series_code)

        remaining_series_codes = [
            series_code for series_code in series_codes if series_code not in yielded_series_codes
        ]
        return remaining_series_codes

    def _get_series_line_iter_context_manager(self) -> AbstractContextManager[TellableStream]:
        series_jsonl_path = self.series_jsonl_path

        if self.revision_id is None:
            try:
                return cast(AbstractContextManager[TellableStream], series_jsonl_path.open("rb"))
            except FileNotFoundError as exc:
                raise SeriesJsonLinesNotFound(dataset_id=self.dataset_id, series_jsonl_path=series_jsonl_path) from exc

        if self._git_provider_directory_manager is None:
            raise RevisionsNotAvailable

        series_jsonl_blob = self._git_provider_directory_manager.load_blob(
            series_jsonl_path, revision_id=self.revision_id
        )
        return nullcontext(TellableStream(series_jsonl_blob.data_stream.stream))

    def _load_json_lines_series_by_seeking(
        self,
        fp: BinaryIO,
        *,
        offset: JsonLinesOffset,
        series_id: SeriesId,
        series_jsonl_path: Path,
        with_observations: bool = True,
    ) -> tuple[JsonLinesSeriesItem, SeriesCode]:
        try:
            fp.seek(offset)
        except Exception as exc:
            raise SeriesJsonLineSeekError(
                offset=offset, series_id=series_id, series_jsonl_path=series_jsonl_path
            ) from exc

        try:
            line = next(fp)
        except Exception as exc:
            raise SeriesJsonLineReadError(
                offset=offset, series_id=series_id, series_jsonl_path=series_jsonl_path
            ) from exc

        try:
            json_lines_series_item = self._parse_json_line_series_item(line, with_observations=with_observations)
        except DataModelError as exc:
            raise SeriesJsonLineParseError(
                offset=offset, series_id=series_id, series_jsonl_path=series_jsonl_path
            ) from exc

        loaded_series_code = SeriesCode.parse(json_lines_series_item.code)
        if loaded_series_code != series_id.series_code:
            raise SeriesJsonLineCodeMismatch(
                loaded_series_code=loaded_series_code,
                offset=offset,
                series_id=series_id,
                series_jsonl_path=series_jsonl_path,
            )

        logger.debug(
            "Loaded series from JSON Lines file by seeking",
            input_file=series_jsonl_path,
            series_id=str(series_id),
            offset=offset,
        )
        return json_lines_series_item, loaded_series_code

    def _parse_json_line_series_item(self, line: bytes, *, with_observations: bool) -> JsonLinesSeriesItem:
        series_jsonl_path = self.series_jsonl_path

        try:
            series_json_data = parse_json_bytes_as_object(line)
        except JsonParseError as exc:
            raise JsonLineParseError(file_path=series_jsonl_path, line=line) from exc

        if not with_observations and "observations" in series_json_data:
            # Delete early to avoid wasting time parsing something that will be deleted later.
            del series_json_data["observations"]

        try:
            return JsonLinesSeriesItem.from_json_data(series_json_data)
        except JsonModelError as exc:
            raise SeriesJsonDataParseError(
                dataset_id=self.dataset_id, series_json_data=series_json_data, series_jsonl_path=series_jsonl_path
            ) from exc
