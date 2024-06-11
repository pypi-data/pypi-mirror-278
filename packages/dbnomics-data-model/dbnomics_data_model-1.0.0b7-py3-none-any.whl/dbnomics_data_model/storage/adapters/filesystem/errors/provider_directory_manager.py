from dbnomics_data_model.model import ProviderCode
from dbnomics_data_model.storage.adapters.filesystem.constants import PROVIDER_JSON
from dbnomics_data_model.storage.adapters.filesystem.errors import FileSystemAdapterError
from dbnomics_data_model.storage.adapters.filesystem.model.provider_json import ProviderJson


class ProviderDirectoryManagerError(FileSystemAdapterError):
    pass


class ProviderJsonCodeMismatch(ProviderDirectoryManagerError):
    def __init__(self, *, expected_provider_code: ProviderCode, provider_json: ProviderJson) -> None:
        msg = f"Expected provider code {expected_provider_code!r} but {PROVIDER_JSON} has {provider_json.code!r}"
        super().__init__(msg=msg)
        self.expected_provider_code = expected_provider_code
        self.provider_json = provider_json
