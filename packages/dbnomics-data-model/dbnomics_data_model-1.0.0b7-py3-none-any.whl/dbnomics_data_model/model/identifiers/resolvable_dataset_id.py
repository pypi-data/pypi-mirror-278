from dataclasses import dataclass
from typing import Self, cast

from parsy import ParseError

from dbnomics_data_model.model.identifiers.errors import ResolvableDatasetIdParseError

from .resolvable_dataset_code import ResolvableDatasetCode
from .types import ProviderCode

__all__ = ["ResolvableDatasetId"]


@dataclass(frozen=True, order=True)
class ResolvableDatasetId:
    provider_code: ProviderCode
    resolvable_dataset_code: ResolvableDatasetCode

    @classmethod
    def create(cls, provider_code: str, resolvable_dataset_code: str) -> Self:
        parsed_provider_code = ProviderCode.parse(provider_code)
        parsed_resolvable_dataset_code = ResolvableDatasetCode.parse(resolvable_dataset_code)
        return cls(parsed_provider_code, parsed_resolvable_dataset_code)

    @classmethod
    def parse(cls, value: str) -> Self:
        from .parsers import resolvable_dataset_id

        try:
            instance = resolvable_dataset_id.parse(value)
        except ParseError as exc:
            raise ResolvableDatasetIdParseError(value=value) from exc

        return cast(Self, instance)

    def __str__(self) -> str:
        return f"{self.provider_code}/{self.resolvable_dataset_code}"
