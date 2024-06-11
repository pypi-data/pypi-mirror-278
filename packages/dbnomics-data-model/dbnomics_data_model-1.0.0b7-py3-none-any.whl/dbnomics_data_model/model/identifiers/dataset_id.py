from dataclasses import dataclass
from typing import Self, cast

from parsy import ParseError

from dbnomics_data_model.model.identifiers.errors import DatasetIdParseError
from dbnomics_data_model.validation.errors.validation_error_data import ValidationErrorPath

from .dataset_code import DatasetCode
from .types import ProviderCode

__all__ = ["DatasetId"]


@dataclass(frozen=True, order=True)
class DatasetId:
    provider_code: ProviderCode
    dataset_code: DatasetCode

    @classmethod
    def create(cls, provider_code: str, dataset_code: str) -> Self:
        parsed_provider_code = ProviderCode.parse(provider_code)
        parsed_dataset_code = DatasetCode.parse(dataset_code)
        return cls(parsed_provider_code, parsed_dataset_code)

    @classmethod
    def parse(cls, value: str) -> Self:
        from .parsers import dataset_id

        try:
            instance = dataset_id.parse(value)
        except ParseError as exc:
            raise DatasetIdParseError(value=value) from exc

        return cast(Self, instance)

    def as_tuple(self) -> tuple[ProviderCode, DatasetCode]:
        return self.provider_code, self.dataset_code

    def __str__(self) -> str:
        return f"{self.provider_code}/{self.dataset_code}"

    @property
    def validation_error_path(self) -> ValidationErrorPath:
        return [
            ("provider_code", str(self.provider_code)),
            ("dataset_code", str(self.dataset_code)),
        ]
