from dataclasses import dataclass, field, replace
from typing import Self

from dbnomics_data_model.model.errors.merge import MergeItemsMismatch
from dbnomics_data_model.model.identifiers import DimensionCode, DimensionValueCode
from dbnomics_data_model.model.merge_utils import merge_iterables_of_items
from dbnomics_data_model.utils import find

from .dimension_value import DimensionValue

__all__ = ["Dimension"]


@dataclass(frozen=True, kw_only=True)
class Dimension:
    code: DimensionCode
    label: str | None = None
    values: list[DimensionValue] = field(default_factory=list)

    @classmethod
    def create(cls, code: str, *, label: str | None = None, values: list[DimensionValue] | None = None) -> Self:
        code = DimensionCode.parse(code)
        if values is None:
            values = []
        return cls(code=code, label=label, values=values)

    def find_value_by_code(self, dimension_value_code: DimensionValueCode) -> DimensionValue | None:
        """Find a dimension value definition by its code."""
        return find(lambda value: value.code == dimension_value_code, self.values, default=None)

    def merge(self, other: "Dimension") -> "Dimension":
        if self.code != other.code:
            raise MergeItemsMismatch(source=other, target=self)

        values = merge_iterables_of_items(
            key=lambda value: value.code,
            merge=lambda _, target: target,
            source=other.values,
            target=self.values,
        )

        return replace(other, values=values)

    @property
    def value_codes(self) -> list[DimensionValueCode]:
        return [dimension_value.code for dimension_value in self.values]
