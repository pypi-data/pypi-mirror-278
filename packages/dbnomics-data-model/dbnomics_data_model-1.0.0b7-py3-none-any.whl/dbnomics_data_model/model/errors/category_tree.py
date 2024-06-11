from typing import TYPE_CHECKING

from dbnomics_data_model.errors import DataModelError
from dbnomics_data_model.model.identifiers import CategoryCode

if TYPE_CHECKING:
    from dbnomics_data_model.model.category_tree.category import Category


class CategoryModelError(DataModelError):
    def __init__(self, *, msg: str, category: "Category") -> None:
        super().__init__(msg=msg)
        self.category = category


class CategoryCodeOrNameRequired(CategoryModelError):
    def __init__(self, *, category: "Category", code: CategoryCode | None, name: str | None) -> None:
        msg = 'Category must have a "code" or a "name", but both are None'
        super().__init__(msg=msg, category=category)
        self.code = code
        self.name = name
