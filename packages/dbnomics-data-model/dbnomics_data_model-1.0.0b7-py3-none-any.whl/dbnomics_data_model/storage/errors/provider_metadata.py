from dbnomics_data_model.errors import DataModelError
from dbnomics_data_model.model import ProviderCode, ProviderMetadata


class ProviderMetadataStorageError(DataModelError):
    def __init__(self, *, msg: str, provider_code: ProviderCode) -> None:
        super().__init__(msg=msg)
        self.provider_code = provider_code


class ProviderMetadataDeleteError(ProviderMetadataStorageError):
    def __init__(self, *, provider_code: ProviderCode) -> None:
        msg = f"Error deleting metadata of provider {provider_code!r}"
        super().__init__(msg=msg, provider_code=provider_code)


class ProviderMetadataLoadError(ProviderMetadataStorageError):
    def __init__(self, *, provider_code: ProviderCode) -> None:
        msg = f"Error loading metadata of provider {provider_code!r}"
        super().__init__(msg=msg, provider_code=provider_code)


class ProviderMetadataNotFound(ProviderMetadataStorageError):
    def __init__(self, *, provider_code: ProviderCode) -> None:
        msg = f"Could not find metadata of provider {provider_code!r}"
        super().__init__(msg=msg, provider_code=provider_code)


class ProviderMetadataSaveError(ProviderMetadataStorageError):
    def __init__(self, *, provider_code: ProviderCode, provider_metadata: ProviderMetadata) -> None:
        msg = f"Error saving metadata of provider {provider_code!r}"
        super().__init__(msg=msg, provider_code=provider_code)
        self.provider_metadata = provider_metadata
