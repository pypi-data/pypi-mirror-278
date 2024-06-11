from dataclasses import dataclass
from typing import Self

from dbnomics_data_model.model.identifiers import DimensionValueCode

__all__ = ["DimensionValue"]


@dataclass(frozen=True, kw_only=True)
class DimensionValue:
    code: DimensionValueCode
    label: str | None = None

    @classmethod
    def create(cls, code: str, *, label: str | None = None) -> Self:
        code = DimensionValueCode.parse(code)
        return cls(code=code, label=label)
