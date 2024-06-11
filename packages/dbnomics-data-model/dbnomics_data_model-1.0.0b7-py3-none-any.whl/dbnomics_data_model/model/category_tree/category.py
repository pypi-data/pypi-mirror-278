from collections.abc import Iterator, Sequence
from dataclasses import dataclass, field, replace
from typing import TYPE_CHECKING, Self

from dbnomics_data_model.model.errors.category_tree import CategoryCodeOrNameRequired
from dbnomics_data_model.model.errors.merge import MergeItemsMismatch
from dbnomics_data_model.model.identifiers import CategoryCode
from dbnomics_data_model.model.url import PublicUrl

from .category_tree_node import CategoryTreeNode, merge_category_tree_nodes

if TYPE_CHECKING:
    from dbnomics_data_model.model.category_tree.dataset_reference import DatasetReference


__all__ = ["Category"]


@dataclass(frozen=True, kw_only=True)
class Category(CategoryTreeNode):
    """A category node of a category tree."""

    children: Sequence[CategoryTreeNode] = field(default_factory=list)
    code: CategoryCode | None = None
    doc_href: PublicUrl | None = None
    name: str | None = None

    def __post_init__(self) -> None:
        code = self.code
        name = self.name
        if code is None and name is None:
            raise CategoryCodeOrNameRequired(category=self, code=code, name=name)

    @classmethod
    def create(
        cls,
        *,
        children: Sequence[CategoryTreeNode] | None = None,
        code: str | None = None,
        name: str | None = None,
        doc_href: str | None = None,
    ) -> Self:
        if code is not None:
            code = CategoryCode.parse(code)
        if children is None:
            children = []
        if doc_href is not None:
            doc_href = PublicUrl.parse(doc_href)
        return cls(children=children, code=code, doc_href=doc_href, name=name)

    def iter_dataset_references(self) -> Iterator["DatasetReference"]:
        for child in self.children:
            yield from child.iter_dataset_references()

    def merge(self, other: "Category") -> "Category":
        if self.code != other.code:
            raise MergeItemsMismatch(source=other, target=self)

        children = merge_category_tree_nodes(source=other.children, target=self.children)
        return replace(other, children=children)

    def __match_key__(self) -> str:
        if self.code is not None:
            return self.code
        assert self.name is not None  # Because of validate_code_or_name_is_defined
        return self.name
