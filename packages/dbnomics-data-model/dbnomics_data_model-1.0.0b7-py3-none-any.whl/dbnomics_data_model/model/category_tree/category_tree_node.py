from abc import ABC, abstractmethod
from collections.abc import Iterable, Iterator
from typing import TYPE_CHECKING

from dbnomics_data_model.model.merge_utils import merge_iterables_of_items

if TYPE_CHECKING:
    from .dataset_reference import DatasetReference


class CategoryTreeNode(ABC):
    @abstractmethod
    def iter_dataset_references(self) -> Iterator["DatasetReference"]:
        """Yield datasets referenced by the nodes recursively."""

    @abstractmethod
    def __match_key__(self) -> str:
        """Return a unique identifier for the category."""


def merge_category_tree_nodes(
    *, source: Iterable[CategoryTreeNode], target: Iterable[CategoryTreeNode]
) -> list[CategoryTreeNode]:
    from .category import Category
    from .dataset_reference import DatasetReference

    def _merge_if_same_node_type(source_node: CategoryTreeNode, target_node: CategoryTreeNode) -> CategoryTreeNode:
        if isinstance(source_node, Category) and isinstance(target_node, Category):
            return target_node.merge(source_node)

        if isinstance(source_node, DatasetReference) and isinstance(target_node, DatasetReference):
            return source_node

        raise NotImplementedError((source_node, target_node))

    return merge_iterables_of_items(
        key=lambda node: node.__match_key__(),
        merge=_merge_if_same_node_type,
        source=source,
        target=target,
    )
