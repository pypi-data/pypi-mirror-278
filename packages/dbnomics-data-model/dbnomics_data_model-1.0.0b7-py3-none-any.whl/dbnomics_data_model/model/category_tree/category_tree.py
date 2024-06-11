from collections.abc import Iterator, Sequence
from dataclasses import dataclass, field, replace

from .category_tree_node import CategoryTreeNode, merge_category_tree_nodes
from .dataset_reference import DatasetReference

__all__ = ["CategoryTree"]


@dataclass(frozen=True, kw_only=True)
class CategoryTree:
    """A category tree referencing datasets."""

    children: Sequence[CategoryTreeNode] = field(default_factory=list)

    def iter_dataset_references(self) -> Iterator[DatasetReference]:
        """Yield datasets referenced by the category tree recursively."""
        for child in self.children:
            yield from child.iter_dataset_references()

    def merge(self, other: "CategoryTree") -> "CategoryTree":
        children = merge_category_tree_nodes(source=other.children, target=self.children)
        return replace(other, children=children)
