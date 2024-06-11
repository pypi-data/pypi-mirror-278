from pathlib import Path
from typing import TYPE_CHECKING, cast

from jsonalias import Json

from dbnomics_data_model.errors import DataModelError
from dbnomics_data_model.validation.errors.validation_error_code_registry import ValidationErrorCodeRegistry
from dbnomics_data_model.validation.errors.validation_error_data import ValidationErrorData

if TYPE_CHECKING:
    from dbnomics_data_model.model.identifiers.series_id import SeriesId

STO001 = ValidationErrorCodeRegistry.register("STO001", description="A series has an invalid TSV file header")


class TsvError(DataModelError):
    pass


class TsvHeaderWriteError(TsvError):
    def __init__(self, fieldnames: list[str], file_path: Path) -> None:
        msg = f"Could not write TSV header to {file_path}"
        super().__init__(msg=msg)
        self.fieldnames = fieldnames
        self.file_path = file_path


class TsvRowWriteError(TsvError):
    def __init__(self, file_path: Path, row: dict[str, str]) -> None:
        msg = f"Could not write TSV row to {file_path}"
        super().__init__(msg=msg)
        self.row = row
        self.file_path = file_path


class InvalidTsvObservationHeader(TsvError):
    def __init__(self, *, header: list[str], series_id: "SeriesId", series_tsv_path: Path) -> None:
        msg = f"The series {str(series_id)!r} has an invalid TSV file header: {header!r}"
        super().__init__(msg=msg)
        self.header = header
        self.series_id = series_id
        self.series_tsv_path = series_tsv_path

    __validation_error_code__ = STO001

    @property
    def __validation_error_data__(self) -> ValidationErrorData:
        header_json = cast(Json, self.header)
        return ValidationErrorData(
            code=self.__validation_error_code__,
            extra={
                "header": header_json,
                "series_tsv_path": str(self.series_tsv_path),
            },
            path=self.series_id.validation_error_path,
        )


class InvalidTsvObservationValue(TsvError):
    pass
