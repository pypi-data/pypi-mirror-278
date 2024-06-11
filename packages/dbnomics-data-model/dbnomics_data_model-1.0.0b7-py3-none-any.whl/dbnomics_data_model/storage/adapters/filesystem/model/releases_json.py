from collections.abc import Iterable
from dataclasses import dataclass, replace
from typing import Self

from dbnomics_data_model.model import DatasetReleases
from dbnomics_data_model.model.errors.merge import MergeItemsMismatch
from dbnomics_data_model.model.merge_utils import merge_iterables_of_items
from dbnomics_data_model.storage.adapters.filesystem.model.base_json_model import BaseJsonObjectModel


@dataclass(kw_only=True)
class ReleasesJson(BaseJsonObjectModel):
    """Model for releases.json.

    Contains dataset release metadata.
    """

    dataset_releases: list["DatasetReleasesJson"]

    def merge_dataset_releases(self, other: Iterable["DatasetReleasesJson"]) -> "ReleasesJson":
        dataset_releases_json_list = merge_iterables_of_items(
            key=lambda dataset_releases_json: dataset_releases_json.dataset_code_prefix,
            merge=lambda source, target: target.merge(source),
            source=other,
            target=self.dataset_releases,
        )
        return ReleasesJson(dataset_releases=dataset_releases_json_list)


@dataclass(kw_only=True)
class DatasetReleasesJson:
    """Dataset releases sharing the same dataset code prefix."""

    dataset_code_prefix: str
    releases: list["ReleaseReferenceJson"]
    name: str | None = None

    @classmethod
    def from_domain_model(cls, dataset_releases: DatasetReleases) -> Self:
        releases = [ReleaseReferenceJson(code=release_code) for release_code in dataset_releases.release_codes]
        return cls(dataset_code_prefix=dataset_releases.bare_dataset_code, releases=releases)

    def merge(self, other: "DatasetReleasesJson") -> "DatasetReleasesJson":
        if self.dataset_code_prefix != other.dataset_code_prefix:
            raise MergeItemsMismatch(source=other, target=self)

        releases = merge_iterables_of_items(
            key=lambda release_reference: release_reference.code,
            merge=lambda _, target: target,
            source=other.releases,
            target=self.releases,
        )

        return replace(other, releases=releases)

    def to_domain_model(self) -> DatasetReleases:
        release_codes = [release.code for release in self.releases]
        return DatasetReleases.create(self.dataset_code_prefix, release_codes=release_codes)


@dataclass(kw_only=True)
class ReleaseReferenceJson:
    code: str
