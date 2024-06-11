from dataclasses import KW_ONLY, dataclass
from typing import Self, cast

from parsy import ParseError

from dbnomics_data_model.model.identifiers.errors import DatasetCodeParseError

from .types import BareDatasetCode, DatasetReleaseCode

__all__ = ["DatasetCode"]


@dataclass(frozen=True, order=True)
class DatasetCode:
    bare_dataset_code: BareDatasetCode

    _: KW_ONLY
    release_code: DatasetReleaseCode | None = None

    # TODO test that it fails with DatasetCode("D1:R1")
    @classmethod
    def create(cls, bare_dataset_code: str, *, release_code: str | None = None) -> Self:
        bare_dataset_code = BareDatasetCode.parse(bare_dataset_code)
        if release_code is not None:
            release_code = DatasetReleaseCode.parse(release_code)
        return cls(bare_dataset_code, release_code=release_code)

    @classmethod
    def parse(cls, value: str) -> Self:
        from .parsers import dataset_code

        try:
            instance = dataset_code.parse(value)
        except ParseError as exc:
            raise DatasetCodeParseError(value=value) from exc

        return cast(Self, instance)

    def __str__(self) -> str:
        result = str(self.bare_dataset_code)
        if self.release_code is not None:
            result += ":" + str(self.release_code)
        return result
