from collections.abc import Sequence
from dataclasses import dataclass, field, replace
from datetime import date, datetime
from typing import Self

from dbnomics_data_model.model.dimensions.dataset_dimensions import DatasetDimensions
from dbnomics_data_model.model.identifiers.attribute_code import AttributeCode
from dbnomics_data_model.model.url import PublicUrl

from .attributes import Attribute
from .errors.merge import MergeItemsMismatch
from .identifiers.dataset_code import DatasetCode
from .merge_utils import merge_iterables_of_items

__all__ = ["DatasetMetadata"]


@dataclass(kw_only=True)
class DatasetMetadata:
    # Attributes are informative and are not used to partition the dataset in groups of time series.
    attributes: list[Attribute] = field(default_factory=list)

    code: DatasetCode
    description: str | None = None

    # Dimensions partition the dataset in groups of time series.
    dimensions: DatasetDimensions = field(default_factory=DatasetDimensions)

    # Set to True if the dataset is no more available on the provider website,
    # or if the provider declares it as discontinued.
    discontinued: bool = False

    # URL to the documentation of the dataset.
    doc_href: PublicUrl | None = None

    name: str | None = None

    # When a new release of the dataset will occur, given by the provider.
    next_release_at: date | datetime | None = None
    notes: list[str] = field(default_factory=list)

    # URL to the page of the dataset on the provider website.
    source_href: PublicUrl | None = None

    # When the dataset was last updated, given by the provider.
    updated_at: date | datetime | None = None

    @classmethod
    def create(
        cls,
        code: DatasetCode | str,
        *,
        attributes: list[Attribute] | None = None,
        description: str | None = None,
        dimensions: DatasetDimensions | None = None,
        discontinued: bool = False,
        doc_href: str | None = None,
        name: str | None = None,
        next_release_at: date | datetime | None = None,
        notes: list[str] | None = None,
        source_href: str | None = None,
        updated_at: date | datetime | None = None,
    ) -> Self:
        if attributes is None:
            attributes = []

        parsed_code = DatasetCode.parse(code) if isinstance(code, str) else code

        if dimensions is None:
            dimensions = DatasetDimensions()

        if doc_href is not None:
            doc_href = PublicUrl.parse(doc_href)

        if notes is None:
            notes = []

        if source_href is not None:
            source_href = PublicUrl.parse(source_href)

        return cls(
            attributes=attributes,
            code=parsed_code,
            description=description,
            dimensions=dimensions,
            discontinued=discontinued,
            doc_href=doc_href,
            name=name,
            next_release_at=next_release_at,
            notes=notes,
            source_href=source_href,
            updated_at=updated_at,
        )

    @property
    def attribute_codes(self) -> Sequence[AttributeCode]:
        return [attribute.code for attribute in self.attributes]

    def merge(self, other: "DatasetMetadata") -> "DatasetMetadata":
        if other.code != self.code:
            raise MergeItemsMismatch(source=other, target=self)

        attributes = merge_iterables_of_items(
            key=lambda attribute: attribute.code,
            merge=lambda source, target: target.merge(source),
            source=other.attributes,
            target=self.attributes,
        )

        dimensions = self.dimensions.merge(other.dimensions)

        return replace(other, attributes=attributes, dimensions=dimensions)
