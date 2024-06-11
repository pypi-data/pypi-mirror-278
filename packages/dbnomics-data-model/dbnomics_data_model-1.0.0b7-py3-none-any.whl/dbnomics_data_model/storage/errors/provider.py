from dbnomics_data_model.errors import DataModelError
from dbnomics_data_model.model import ProviderCode


class ProviderStorageError(DataModelError):
    def __init__(self, *, msg: str, provider_code: ProviderCode) -> None:
        super().__init__(msg=msg)
        self.provider_code = provider_code


class ProviderDeleteError(ProviderStorageError):
    def __init__(self, *, provider_code: ProviderCode) -> None:
        msg = f"Error deleting provider {provider_code!r}"
        super().__init__(msg=msg, provider_code=provider_code)


class ProviderNotFound(ProviderStorageError):
    def __init__(self, *, provider_code: ProviderCode) -> None:
        msg = f"Could not find provider {provider_code!r}"
        super().__init__(msg=msg, provider_code=provider_code)
