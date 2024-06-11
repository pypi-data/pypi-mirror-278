from dbnomics_data_model.errors import DataModelError
from dbnomics_data_model.model.identifiers import ProviderCode
from dbnomics_data_model.model.provider_metadata import ProviderMetadata


class ProviderMetadataModelError(DataModelError):
    def __init__(self, *, msg: str, provider_metadata: ProviderMetadata) -> None:
        super().__init__(msg=msg)
        self.provider_metadata = provider_metadata


class ProviderMetadataCodeMismatch(ProviderMetadataModelError):
    def __init__(self, *, expected_provider_code: ProviderCode, provider_metadata: ProviderMetadata) -> None:
        msg = f"Expected provider code {expected_provider_code!r} but model instance has {provider_metadata.code!r}"
        super().__init__(msg=msg, provider_metadata=provider_metadata)
        self.expected_provider_code = expected_provider_code
