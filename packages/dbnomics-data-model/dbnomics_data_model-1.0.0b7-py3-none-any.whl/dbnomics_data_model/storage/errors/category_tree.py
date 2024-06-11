from dbnomics_data_model.errors import DataModelError
from dbnomics_data_model.model import CategoryTree, ProviderCode


class CategoryTreeStorageError(DataModelError):
    def __init__(self, *, msg: str, provider_code: ProviderCode) -> None:
        super().__init__(msg=msg)
        self.provider_code = provider_code


class CategoryTreeDeleteError(CategoryTreeStorageError):
    def __init__(self, *, provider_code: ProviderCode) -> None:
        msg = f"Error deleting category tree of provider {provider_code!r}"
        super().__init__(msg=msg, provider_code=provider_code)


class CategoryTreeLoadError(CategoryTreeStorageError):
    def __init__(self, *, provider_code: ProviderCode) -> None:
        msg = f"Error loading category tree of provider {provider_code!r}"
        super().__init__(msg=msg, provider_code=provider_code)


class CategoryTreeNotFound(CategoryTreeStorageError):
    def __init__(self, *, provider_code: ProviderCode) -> None:
        msg = f"Could not find category tree of provider {provider_code!r}"
        super().__init__(msg=msg, provider_code=provider_code)


class CategoryTreeSaveError(CategoryTreeStorageError):
    def __init__(self, *, category_tree: CategoryTree, provider_code: ProviderCode) -> None:
        msg = f"Error saving category tree of provider {provider_code!r}"
        super().__init__(msg=msg, provider_code=provider_code)
        self.category_tree = category_tree
