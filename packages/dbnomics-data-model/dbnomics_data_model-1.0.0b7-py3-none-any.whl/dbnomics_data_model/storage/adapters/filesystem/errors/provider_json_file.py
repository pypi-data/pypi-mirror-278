from pathlib import Path

from dbnomics_data_model.model import ProviderCode
from dbnomics_data_model.storage.adapters.filesystem.errors import FileSystemAdapterError
from dbnomics_data_model.storage.adapters.filesystem.model.provider_json import ProviderJson


class ProviderJsonFileError(FileSystemAdapterError):
    def __init__(self, *, msg: str, provider_code: ProviderCode, provider_json_path: Path) -> None:
        super().__init__(msg=msg)
        self.provider_code = provider_code
        self.provider_json_path = provider_json_path


class ProviderJsonDeleteError(ProviderJsonFileError):
    def __init__(self, *, provider_code: ProviderCode, provider_json_path: Path) -> None:
        msg = f"Error deleting {provider_json_path} of provider {provider_code!r}"
        super().__init__(msg=msg, provider_code=provider_code, provider_json_path=provider_json_path)


class ProviderJsonLoadError(ProviderJsonFileError):
    def __init__(self, *, provider_code: ProviderCode, provider_json_path: Path) -> None:
        msg = f"Error loading {provider_json_path} of provider {provider_code!r}"
        super().__init__(msg=msg, provider_code=provider_code, provider_json_path=provider_json_path)


class ProviderJsonNotFound(ProviderJsonFileError):
    def __init__(self, *, provider_code: ProviderCode, provider_json_path: Path) -> None:
        msg = f"Could not find {provider_json_path} of provider {provider_code!r}"
        super().__init__(msg=msg, provider_code=provider_code, provider_json_path=provider_json_path)


class ProviderJsonSaveError(ProviderJsonFileError):
    def __init__(self, *, provider_code: ProviderCode, provider_json: ProviderJson, provider_json_path: Path) -> None:
        msg = f"Error saving {provider_json_path} of provider {provider_code!r}"
        super().__init__(msg=msg, provider_code=provider_code, provider_json_path=provider_json_path)
        self.provider_json = provider_json
