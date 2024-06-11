from dataclasses import KW_ONLY, dataclass
from typing import Self, cast

from parsy import ParseError

from dbnomics_data_model.model.constants import LATEST_RELEASE
from dbnomics_data_model.model.identifiers.errors import ResolvableDatasetCodeParseError

from .types import BareDatasetCode, DatasetReleaseCode, ResolvableDatasetReleaseCode

__all__ = ["ResolvableDatasetCode"]


@dataclass(frozen=True, order=True)
class ResolvableDatasetCode:
    bare_dataset_code: BareDatasetCode

    _: KW_ONLY
    resolvable_release_code: ResolvableDatasetReleaseCode | None

    @classmethod
    def create(cls, bare_dataset_code: str, *, resolvable_release_code: str | None = None) -> Self:
        bare_dataset_code = BareDatasetCode.parse(bare_dataset_code)
        if resolvable_release_code is not None and resolvable_release_code != LATEST_RELEASE:
            resolvable_release_code = DatasetReleaseCode.parse(resolvable_release_code)
        return cls(
            bare_dataset_code,
            resolvable_release_code=cast(ResolvableDatasetReleaseCode | None, resolvable_release_code),
        )

    @classmethod
    def parse(cls, value: str) -> Self:
        from .parsers import resolvable_dataset_code

        try:
            instance = resolvable_dataset_code.parse(value)
        except ParseError as exc:
            raise ResolvableDatasetCodeParseError(value=value) from exc

        return cast(Self, instance)

    def __str__(self) -> str:
        result = str(self.bare_dataset_code)
        if self.resolvable_release_code is not None:
            result += ":" + str(self.resolvable_release_code)
        return result
