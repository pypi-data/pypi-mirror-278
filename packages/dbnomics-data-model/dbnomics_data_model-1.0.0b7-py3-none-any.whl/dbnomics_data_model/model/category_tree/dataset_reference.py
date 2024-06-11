from collections.abc import Iterator
from dataclasses import dataclass
from typing import Self

from dbnomics_data_model.model.category_tree.category_tree_node import CategoryTreeNode
from dbnomics_data_model.model.identifiers.dataset_code import DatasetCode

__all__ = ["DatasetReference"]


@dataclass(frozen=True, kw_only=True)
class DatasetReference(CategoryTreeNode):
    """A dataset node of a category tree."""

    code: DatasetCode
    name: str | None = None

    @classmethod
    def create(cls, code: str, *, name: str | None = None) -> Self:
        parsed_code = DatasetCode.parse(code)
        return cls(code=parsed_code, name=name)

    def iter_dataset_references(self) -> Iterator["DatasetReference"]:
        yield self

    def __match_key__(self) -> str:
        return str(self.code)
