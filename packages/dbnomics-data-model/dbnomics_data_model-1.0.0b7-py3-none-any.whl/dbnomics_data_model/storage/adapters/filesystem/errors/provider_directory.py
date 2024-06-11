from pathlib import Path

from dbnomics_data_model.model import ProviderCode
from dbnomics_data_model.storage.adapters.filesystem.errors import FileSystemAdapterError


class ProviderDirectoryError(FileSystemAdapterError):
    def __init__(self, *, msg: str, provider_code: ProviderCode, provider_dir: Path) -> None:
        super().__init__(msg=msg)
        self.provider_code = provider_code
        self.provider_dir = provider_dir


class ProviderDirectoryDeleteError(ProviderDirectoryError):
    def __init__(self, *, provider_code: ProviderCode, provider_dir: Path) -> None:
        msg = f"Error deleting the directory of provider {provider_code!r}: {provider_dir}"
        super().__init__(msg=msg, provider_code=provider_code, provider_dir=provider_dir)


class ProviderDirectoryNotFound(ProviderDirectoryError):
    def __init__(self, *, provider_code: ProviderCode, provider_dir: Path) -> None:
        msg = f"Could not find the directory of provider {provider_code!r}: {provider_dir}"
        super().__init__(msg=msg, provider_code=provider_code, provider_dir=provider_dir)
