from dataclasses import dataclass, replace
from typing import Self

from dbnomics_data_model.model.errors.merge import MergeItemsMismatch
from dbnomics_data_model.model.identifiers.attribute_code import AttributeCode
from dbnomics_data_model.model.merge_utils import merge_iterables_of_items

from .attribute_value import AttributeValue

__all__ = ["Attribute"]


@dataclass(frozen=True, kw_only=True)
class Attribute:
    code: AttributeCode
    label: str | None = None
    values: list[AttributeValue] | None = None

    @classmethod
    def create(cls, code: str, *, label: str | None = None, values: list[AttributeValue] | None = None) -> Self:
        code = AttributeCode.parse(code)
        return cls(code=code, label=label, values=values)

    def merge(self, other: "Attribute") -> "Attribute":
        if self.code != other.code:
            raise MergeItemsMismatch(source=other, target=self)

        if self.values is not None and other.values is not None:
            values = merge_iterables_of_items(
                key=lambda value: value.code,
                merge=lambda _, target: target,
                source=other.values,
                target=self.values,
            )
            return replace(other, values=values)

        return other
