from dbnomics_data_model.model.identifiers import ProviderCode
from dbnomics_data_model.storage.adapters.filesystem.errors import FileSystemAdapterError


class SingleProviderFileSystemStorageError(FileSystemAdapterError):
    pass


class ProviderCodeMismatch(SingleProviderFileSystemStorageError):
    def __init__(self, *, expected_provider_code: ProviderCode, provider_code: ProviderCode) -> None:
        msg = f"Expected provider code {expected_provider_code!r} but got {provider_code!r}"
        super().__init__(msg=msg)
        self.expected_provider_code = expected_provider_code
        self.provider_code = provider_code
