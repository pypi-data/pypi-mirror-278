from dataclasses import dataclass, replace
from typing import Self

from dbnomics_data_model.model.constants import LATEST_RELEASE
from dbnomics_data_model.model.errors.merge import MergeItemsMismatch
from dbnomics_data_model.model.identifiers import BareDatasetCode, DatasetReleaseCode, ResolvableDatasetReleaseCode

from .errors.dataset_releases import DatasetReleasesHasNoReleaseCodes

__all__ = ["DatasetReleases"]


@dataclass(kw_only=True)
class DatasetReleases:
    """Dataset releases sharing a common bare dataset code."""

    bare_dataset_code: BareDatasetCode
    release_codes: list[DatasetReleaseCode]

    def __post_init__(self) -> None:
        if not self.release_codes:
            raise DatasetReleasesHasNoReleaseCodes(dataset_releases=self)

    @classmethod
    def create(cls, bare_dataset_code: str, *, release_codes: list[str]) -> Self:
        bare_dataset_code = BareDatasetCode.parse(bare_dataset_code)
        parsed_release_codes = [DatasetReleaseCode.parse(release_code) for release_code in release_codes]
        return cls(bare_dataset_code=bare_dataset_code, release_codes=parsed_release_codes)

    def find_latest_release_code(self) -> DatasetReleaseCode:
        assert self.release_codes
        return self.release_codes[-1]

    def merge(self, other: "DatasetReleases") -> "DatasetReleases":
        if self.bare_dataset_code != other.bare_dataset_code:
            raise MergeItemsMismatch(source=other, target=self)

        # Keep release codes order
        # TODO create specific test for this
        kept_release_codes = [
            release_code for release_code in self.release_codes if release_code not in other.release_codes
        ]
        release_codes = [*kept_release_codes, *other.release_codes]

        return replace(other, release_codes=release_codes)

    def resolve_release_code(self, resolvable_release_code: ResolvableDatasetReleaseCode) -> DatasetReleaseCode:
        if resolvable_release_code != LATEST_RELEASE:
            return resolvable_release_code

        return self.find_latest_release_code()
