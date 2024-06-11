from dataclasses import dataclass
from typing import Self, cast

from parsy import ParseError

from dbnomics_data_model.model.identifiers.errors import BareDatasetIdParseError

from .types import BareDatasetCode, ProviderCode

__all__ = ["BareDatasetId"]


@dataclass(frozen=True, order=True)
class BareDatasetId:
    provider_code: ProviderCode
    bare_dataset_code: BareDatasetCode

    @classmethod
    def create(cls, provider_code: str, bare_dataset_code: str) -> Self:
        provider_code = ProviderCode.parse(provider_code)
        bare_dataset_code = BareDatasetCode.parse(bare_dataset_code)
        return cls(provider_code, bare_dataset_code)

    @classmethod
    def parse(cls, value: str) -> Self:
        from .parsers import bare_dataset_id

        try:
            instance = bare_dataset_id.parse(value)
        except ParseError as exc:
            raise BareDatasetIdParseError(value=value) from exc

        return cast(Self, instance)

    def __str__(self) -> str:
        return f"{self.provider_code}/{self.bare_dataset_code}"
