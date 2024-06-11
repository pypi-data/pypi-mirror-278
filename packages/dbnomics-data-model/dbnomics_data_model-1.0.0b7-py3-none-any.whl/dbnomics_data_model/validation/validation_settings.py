from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass, field, replace
from typing import Self

from dbnomics_data_model.validation.errors.validation_error_code import ValidationErrorCode


@dataclass(frozen=True, kw_only=True)
class ValidationSettings:
    disable_series_validation: bool = False
    disabled_codes: set[ValidationErrorCode] = field(default_factory=set)

    def disable(self, codes: set[ValidationErrorCode]) -> Self:
        return replace(self, disabled_codes=self.disabled_codes | codes)

    def is_any_validation_code_enabled(self, *codes: ValidationErrorCode) -> bool:
        return any(self.is_validation_code_enabled(code) for code in codes)

    def is_validation_code_enabled(self, code: ValidationErrorCode) -> bool:
        return code not in self.disabled_codes


current_validation_settings_var: ContextVar[ValidationSettings] = ContextVar(
    "validation_settings", default=ValidationSettings()
)


@contextmanager
def overridden_validation_settings(
    disable_series_validation: bool | None = None,
    disabled_codes: set[ValidationErrorCode] | None = None,
) -> Iterator[None]:
    validation_settings = current_validation_settings_var.get()

    new_validation_settings = validation_settings
    if disable_series_validation is not None:
        new_validation_settings = replace(new_validation_settings, disable_series_validation=disable_series_validation)
    if disabled_codes is not None:
        new_validation_settings = new_validation_settings.disable(disabled_codes)

    token = current_validation_settings_var.set(new_validation_settings)
    yield
    current_validation_settings_var.reset(token)
