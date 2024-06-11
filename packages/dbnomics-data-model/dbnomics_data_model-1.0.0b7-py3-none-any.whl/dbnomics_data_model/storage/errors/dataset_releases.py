from dbnomics_data_model.errors import DataModelError
from dbnomics_data_model.model import DatasetReleases, ProviderCode


class DatasetReleasesStorageError(DataModelError):
    def __init__(self, *, msg: str, provider_code: ProviderCode) -> None:
        super().__init__(msg=msg)
        self.provider_code = provider_code


class DatasetReleasesDeleteError(DatasetReleasesStorageError):
    def __init__(self, *, provider_code: ProviderCode) -> None:
        msg = f"Error deleting dataset releases of provider {provider_code!r}"
        super().__init__(msg=msg, provider_code=provider_code)


class DatasetReleasesLoadError(DatasetReleasesStorageError):
    def __init__(self, *, provider_code: ProviderCode) -> None:
        msg = f"Error loading dataset releases of provider {provider_code!r}"
        super().__init__(msg=msg, provider_code=provider_code)


class DatasetReleasesNotFound(DatasetReleasesStorageError):
    def __init__(self, *, provider_code: ProviderCode) -> None:
        msg = f"Could not find dataset releases of provider {provider_code!r}"
        super().__init__(msg=msg, provider_code=provider_code)


class DatasetReleasesSaveError(DatasetReleasesStorageError):
    def __init__(self, *, dataset_releases_list: list[DatasetReleases], provider_code: ProviderCode) -> None:
        msg = f"Error saving dataset releases of provider {provider_code!r}"
        super().__init__(msg=msg, provider_code=provider_code)
        self.dataset_releases_list = dataset_releases_list
