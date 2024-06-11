from dataclasses import dataclass
from typing import ClassVar

from dbnomics_data_model.validation.errors.validation_error_level import ValidationErrorLevel

from .validation_error_code import ValidationErrorCode


@dataclass(frozen=True, kw_only=True)
class ValidationErrorCodeInfo:
    description: str
    level: ValidationErrorLevel = ValidationErrorLevel.ERROR


class ValidationErrorCodeRegistry:
    _requested_error_codes: ClassVar[dict[ValidationErrorCode, ValidationErrorCodeInfo]] = {}

    @classmethod
    def get(cls, code: ValidationErrorCode) -> ValidationErrorCodeInfo:
        return cls._requested_error_codes[code]

    @classmethod
    def register(cls, value: str, *, description: str) -> ValidationErrorCode:
        error_code = ValidationErrorCode.parse(value)
        if error_code in cls._requested_error_codes:
            msg = f"Error code {error_code} has already been registered"
            raise KeyError(msg)

        cls._requested_error_codes[error_code] = ValidationErrorCodeInfo(description=description)
        return error_code
