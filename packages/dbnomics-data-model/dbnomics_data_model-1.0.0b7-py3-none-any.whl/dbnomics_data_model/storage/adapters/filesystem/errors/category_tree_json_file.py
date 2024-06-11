from pathlib import Path

from dbnomics_data_model.model import ProviderCode
from dbnomics_data_model.storage.adapters.filesystem.errors import FileSystemAdapterError
from dbnomics_data_model.storage.adapters.filesystem.model.category_tree_json import CategoryTreeJson


class CategoryTreeJsonFileError(FileSystemAdapterError):
    def __init__(self, *, category_tree_json_path: Path, msg: str, provider_code: ProviderCode) -> None:
        super().__init__(msg=msg)
        self.category_tree_json_path = category_tree_json_path
        self.provider_code = provider_code


class CategoryTreeJsonDeleteError(CategoryTreeJsonFileError):
    def __init__(self, *, category_tree_json_path: Path, provider_code: ProviderCode) -> None:
        msg = f"Error deleting {category_tree_json_path} of provider {provider_code!r}"
        super().__init__(category_tree_json_path=category_tree_json_path, msg=msg, provider_code=provider_code)


class CategoryTreeJsonLoadError(CategoryTreeJsonFileError):
    def __init__(self, *, category_tree_json_path: Path, provider_code: ProviderCode) -> None:
        msg = f"Error loading {category_tree_json_path} of provider {provider_code!r}"
        super().__init__(category_tree_json_path=category_tree_json_path, msg=msg, provider_code=provider_code)


class CategoryTreeJsonNotFound(CategoryTreeJsonFileError):
    def __init__(self, *, category_tree_json_path: Path, provider_code: ProviderCode) -> None:
        msg = f"Could not find {category_tree_json_path} of provider {provider_code!r}"
        super().__init__(category_tree_json_path=category_tree_json_path, msg=msg, provider_code=provider_code)


class CategoryTreeJsonSaveError(CategoryTreeJsonFileError):
    def __init__(
        self, *, category_tree_json: CategoryTreeJson, category_tree_json_path: Path, provider_code: ProviderCode
    ) -> None:
        msg = f"Error saving {category_tree_json_path} of provider {provider_code!r}"
        super().__init__(category_tree_json_path=category_tree_json_path, msg=msg, provider_code=provider_code)
        self.category_tree_json = category_tree_json
