from dataclasses import dataclass
from typing import Self

from dbnomics_data_model.model.identifiers.types import AttributeValueCode

__all__ = ["AttributeValue"]


@dataclass(frozen=True, kw_only=True)
class AttributeValue:
    code: AttributeValueCode
    label: str | None = None

    @classmethod
    def create(cls, code: str, *, label: str | None = None) -> Self:
        code = AttributeValueCode.parse(code)
        return cls(code=code, label=label)
