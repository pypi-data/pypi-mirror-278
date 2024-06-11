from dataclasses import dataclass
from typing import Self, cast

from parsy import ParseError

from dbnomics_data_model.model.identifiers.errors import SeriesIdParseError
from dbnomics_data_model.validation.errors.validation_error_data import ValidationErrorPath

from .dataset_code import DatasetCode
from .dataset_id import DatasetId
from .series_code import SeriesCode
from .types import ProviderCode

__all__ = ["SeriesId"]


@dataclass(frozen=True, order=True)
class SeriesId:
    provider_code: ProviderCode
    dataset_code: DatasetCode
    series_code: SeriesCode

    @classmethod
    def create(cls, provider_code: str, dataset_code: str, series_code: str) -> Self:
        parsed_provider_code = ProviderCode.parse(provider_code)
        parsed_dataset_code = DatasetCode.parse(dataset_code)
        parsed_series_code = SeriesCode.parse(series_code)
        return cls(parsed_provider_code, parsed_dataset_code, parsed_series_code)

    @classmethod
    def from_dataset_id(cls, dataset_id: DatasetId, series_code: SeriesCode) -> Self:
        return cls(dataset_id.provider_code, dataset_id.dataset_code, series_code)

    @classmethod
    def parse(cls, value: str) -> Self:
        from .parsers import series_id

        try:
            instance = series_id.parse(value)
        except ParseError as exc:
            raise SeriesIdParseError(value=value) from exc

        return cast(Self, instance)

    def as_tuple(self) -> tuple[ProviderCode, DatasetCode, SeriesCode]:
        return self.provider_code, self.dataset_code, self.series_code

    def __str__(self) -> str:
        return f"{self.provider_code}/{self.dataset_code}/{self.series_code}"

    @property
    def dataset_id(self) -> DatasetId:
        return DatasetId(self.provider_code, self.dataset_code)

    @property
    def validation_error_path(self) -> ValidationErrorPath:
        return [
            ("provider_code", str(self.provider_code)),
            ("dataset_code", str(self.dataset_code)),
            ("series_code", str(self.series_code)),
        ]
