from pathlib import Path

from dbnomics_data_model.model import ProviderCode
from dbnomics_data_model.storage.adapters.filesystem.errors import FileSystemAdapterError
from dbnomics_data_model.storage.adapters.filesystem.model.releases_json import ReleasesJson


class ReleasesJsonFileError(FileSystemAdapterError):
    def __init__(self, *, msg: str, provider_code: ProviderCode, releases_json_path: Path) -> None:
        super().__init__(msg=msg)
        self.releases_json_path = releases_json_path
        self.provider_code = provider_code


class ReleasesJsonDeleteError(ReleasesJsonFileError):
    def __init__(self, *, provider_code: ProviderCode, releases_json_path: Path) -> None:
        msg = f"Error deleting {releases_json_path} of provider {provider_code!r}"
        super().__init__(releases_json_path=releases_json_path, msg=msg, provider_code=provider_code)


class ReleasesJsonLoadError(ReleasesJsonFileError):
    def __init__(self, *, provider_code: ProviderCode, releases_json_path: Path) -> None:
        msg = f"Error loading {releases_json_path} of provider {provider_code!r}"
        super().__init__(releases_json_path=releases_json_path, msg=msg, provider_code=provider_code)


class ReleasesJsonNotFound(ReleasesJsonFileError):
    def __init__(self, *, provider_code: ProviderCode, releases_json_path: Path) -> None:
        msg = f"Could not find {releases_json_path} of provider {provider_code!r}"
        super().__init__(releases_json_path=releases_json_path, msg=msg, provider_code=provider_code)


class ReleasesJsonSaveError(ReleasesJsonFileError):
    def __init__(self, *, provider_code: ProviderCode, releases_json: ReleasesJson, releases_json_path: Path) -> None:
        msg = f"Error saving {releases_json_path} of provider {provider_code!r}"
        super().__init__(releases_json_path=releases_json_path, msg=msg, provider_code=provider_code)
        self.releases_json = releases_json
