from dataclasses import KW_ONLY, dataclass

from dbnomics_data_model.validation.errors.validation_error_data import ValidationErrorPath

from .dataset_id import DatasetId
from .series_code import SeriesCode

__all__ = ["SeriesCodeOrId"]


@dataclass(frozen=True, order=True)
class SeriesCodeOrId:
    series_code: SeriesCode

    _: KW_ONLY
    dataset_id: DatasetId | None

    def __str__(self) -> str:
        return str(self.series_code) if self.dataset_id is None else f"{self.dataset_id}/{self.series_code}"

    @property
    def validation_error_path(self) -> ValidationErrorPath:
        result = []
        if self.dataset_id is not None:
            result.extend(self.dataset_id.validation_error_path)
        result.append(("series_code", str(self.series_code)))
        return result
