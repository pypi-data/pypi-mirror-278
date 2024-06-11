from typing import TYPE_CHECKING

from dbnomics_data_model.errors import DataModelError
from dbnomics_data_model.model.identifiers.bare_dataset_id import BareDatasetId

if TYPE_CHECKING:
    from dbnomics_data_model.model.dataset_releases import DatasetReleases


class DatasetHasNoRelease(DataModelError):
    def __init__(self, bare_dataset_id: BareDatasetId) -> None:
        msg = f"The dataset {str(bare_dataset_id)!r} does not have any release"
        super().__init__(msg=msg)
        self.bare_dataset_id = bare_dataset_id


class DatasetReleasesModelError(DataModelError):
    def __init__(self, *, dataset_releases: "DatasetReleases", msg: str) -> None:
        super().__init__(msg=msg)
        self.dataset_releases = dataset_releases


class DatasetReleasesHasNoReleaseCodes(DatasetReleasesModelError):
    def __init__(self, *, dataset_releases: "DatasetReleases") -> None:
        msg = "DatasetReleases must define at least a release code"
        super().__init__(dataset_releases=dataset_releases, msg=msg)
