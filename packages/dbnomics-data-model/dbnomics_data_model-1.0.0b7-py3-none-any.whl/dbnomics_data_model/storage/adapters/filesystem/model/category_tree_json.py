from dataclasses import dataclass
from typing import List, Self, TypeAlias  # noqa: UP035

from jsonalias import Json

from dbnomics_data_model.json_utils.errors import JsonParseTypeError
from dbnomics_data_model.json_utils.parsing import parse_json_data
from dbnomics_data_model.model import Category, CategoryTree, CategoryTreeNode, DatasetReference
from dbnomics_data_model.storage.adapters.filesystem.errors.json_model import JsonModelParseError

from .base_json_model import BaseJsonObjectModel


@dataclass(kw_only=True)
class DatasetReferenceJson(BaseJsonObjectModel):
    """Model for a dataset reference of category_tree.json."""

    code: str
    name: str | None = None

    @classmethod
    def from_domain_model(cls, dataset_reference: DatasetReference) -> Self:
        return cls(code=str(dataset_reference.code), name=dataset_reference.name)

    def to_domain_model(self) -> DatasetReference:
        return DatasetReference.create(self.code, name=self.name)


@dataclass(kw_only=True)
class CategoryJson(BaseJsonObjectModel):
    """Model for a category node of category_tree.json."""

    children: List["CategoryTreeNodeJson"]  # noqa: UP006
    code: str | None = None
    name: str | None = None
    doc_href: str | None = None

    @classmethod
    def from_domain_model(cls, category: Category) -> Self:
        return cls(
            children=[node_from_domain_model(child) for child in category.children],
            code=category.code,
            doc_href=category.doc_href,
            name=category.name,
        )

    def to_domain_model(self) -> Category:
        children: list[CategoryTreeNode] = [node.to_domain_model() for node in self.children]
        return Category.create(children=children, code=self.code, doc_href=self.doc_href, name=self.name)


CategoryTreeNodeJson: TypeAlias = CategoryJson | DatasetReferenceJson


def node_from_domain_model(node: CategoryTreeNode) -> CategoryTreeNodeJson:
    if isinstance(node, Category):
        return CategoryJson.from_domain_model(node)

    assert isinstance(node, DatasetReference)

    return DatasetReferenceJson.from_domain_model(node)


@dataclass(kw_only=True)
class CategoryTreeJson:
    """Model for category_tree.json."""

    nodes: List[CategoryTreeNodeJson]  # noqa: UP006

    @classmethod
    def from_domain_model(cls, category_tree: CategoryTree) -> Self:
        nodes = [node_from_domain_model(node) for node in category_tree.children]
        return cls(nodes=nodes)

    @classmethod
    def from_json_data(cls, data: Json) -> Self:
        try:
            nodes = parse_json_data(data, type_=List[CategoryTreeNodeJson])  # noqa: UP006
        except JsonParseTypeError as exc:
            raise JsonModelParseError(data=data) from exc

        return cls(nodes=nodes)

    def to_domain_model(self) -> CategoryTree:
        return CategoryTree(children=[node.to_domain_model() for node in self.nodes])

    def to_json_data(self) -> list[Json]:
        return [node.to_json_data() for node in self.nodes]
