from collections.abc import Iterator
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import TypeVar

from dbnomics_data_model.model import Attribute, DatasetMetadata
from dbnomics_data_model.model.attributes.attribute_value import AttributeValue
from dbnomics_data_model.model.dimensions.dataset_dimensions import DatasetDimensions
from dbnomics_data_model.model.dimensions.dimension import Dimension
from dbnomics_data_model.model.dimensions.dimension_value import DimensionValue
from dbnomics_data_model.model.identifiers.errors import SimpleCodeParseError
from dbnomics_data_model.storage.adapters.filesystem.errors.json_model import JsonModelError
from dbnomics_data_model.storage.adapters.filesystem.model.base_json_model import BaseJsonObjectModel
from dbnomics_data_model.storage.adapters.filesystem.model.errors.base_dataset_json import (
    DimensionValueCreateError,
    UnusedDimensionLabelsKeys,
    UnusedDimensionValueLabelsKeys,
)

TBaseDatasetJson = TypeVar("TBaseDatasetJson", bound="BaseDatasetJson")


@dataclass(kw_only=True)
class BaseDatasetJson(BaseJsonObjectModel):
    """Base model for dataset.json.

    Is subclassed to model JSON Lines and TSV variants.
    """

    code: str

    attributes_labels: dict[str, str | None] = field(default_factory=dict)
    attributes_values_labels: dict[str, dict[str, str | None]] = field(default_factory=dict)
    description: str | None = None
    dimensions_codes_order: list[str] | None = None
    dimensions_labels: dict[str, str | None] = field(default_factory=dict)
    dimensions_values_labels: dict[str, dict[str, str | None]] | dict[str, list[tuple[str, str | None]]] = field(
        default_factory=dict[str, dict[str, str | None]]
    )
    discontinued: bool = False
    doc_href: str | None = None
    name: str | None = None
    next_release_at: date | datetime | None = None
    notes: list[str] | None = None
    source_href: str | None = None
    updated_at: date | datetime | None = None

    @classmethod
    def from_domain_model(cls: type[TBaseDatasetJson], dataset_metadata: DatasetMetadata) -> TBaseDatasetJson:
        return cls(
            attributes_labels=cls._build_attributes_labels(dataset_metadata),
            attributes_values_labels=cls._build_attributes_values_labels(dataset_metadata),
            code=str(dataset_metadata.code),
            description=dataset_metadata.description,
            dimensions_codes_order=cls._build_dimensions_codes_order(dataset_metadata),
            dimensions_labels=cls._build_dimensions_labels(dataset_metadata),
            dimensions_values_labels=cls._build_dimensions_values_labels(dataset_metadata),
            discontinued=dataset_metadata.discontinued,
            doc_href=dataset_metadata.doc_href,
            name=dataset_metadata.name,
            next_release_at=dataset_metadata.next_release_at,
            notes=dataset_metadata.notes,
            source_href=dataset_metadata.source_href,
            updated_at=dataset_metadata.updated_at,
        )

    @property
    def attribute_codes(self) -> list[str]:
        return sorted(set(self.attributes_labels.keys()) | set(self.attributes_values_labels.keys()))

    def to_domain_model(self) -> DatasetMetadata:
        attributes = list(self._iter_attributes_as_domain_model())
        dimensions = DatasetDimensions(list(self._iter_dimensions_as_domain_model()))
        return DatasetMetadata.create(
            self.code,
            attributes=attributes,
            description=self.description,
            dimensions=dimensions,
            discontinued=self.discontinued,
            doc_href=self.doc_href,
            name=self.name,
            next_release_at=self.next_release_at,
            notes=self.notes,
            source_href=self.source_href,
            updated_at=self.updated_at,
        )

    def validate(self) -> Iterator[JsonModelError]:
        yield from self.validate_dimensions_labels()
        yield from self.validate_dimensions_values_labels()

    def validate_dimensions_labels(self) -> Iterator[UnusedDimensionLabelsKeys]:
        """Validate the keys of the `dimensions_labels` attribute.

        Check that every key of `dimensions_labels` is defined in `dimensions_codes_order`, if it's defined.
        """
        dimensions_codes_order = self.dimensions_codes_order
        if dimensions_codes_order is None:
            return

        dimension_codes = set(self.dimensions_labels.keys())
        unused_dimension_codes = dimension_codes - set(dimensions_codes_order)
        if unused_dimension_codes:
            yield UnusedDimensionLabelsKeys(dataset_json=self, unused_dimension_codes=unused_dimension_codes)

    def validate_dimensions_values_labels(self) -> Iterator[UnusedDimensionValueLabelsKeys]:
        """Validate the keys of the `dimensions_values_labels` attribute.

        Check that every key of `dimensions_values_labels` is defined in `dimensions_codes_order`, if it's defined.
        """
        dimensions_codes_order = self.dimensions_codes_order
        if dimensions_codes_order is None:
            return

        dimension_codes = set(self.dimensions_values_labels.keys())
        unused_dimension_codes = dimension_codes - set(dimensions_codes_order)
        if unused_dimension_codes:
            yield UnusedDimensionValueLabelsKeys(dataset_json=self, unused_dimension_codes=unused_dimension_codes)

    @classmethod
    def _build_attributes_labels(cls, dataset_metadata: DatasetMetadata) -> dict[str, str | None]:
        return {str(attribute.code): attribute.label for attribute in dataset_metadata.attributes}

    @classmethod
    def _build_attributes_values_labels(cls, dataset_metadata: DatasetMetadata) -> dict[str, dict[str, str | None]]:
        return {
            attribute.code: {value.code: value.label for value in attribute.values}
            for attribute in dataset_metadata.attributes
            if attribute.values
        }

    @classmethod
    def _build_dimensions_codes_order(cls, dataset_metadata: DatasetMetadata) -> list[str]:
        return [dimension.code for dimension in dataset_metadata.dimensions]

    @classmethod
    def _build_dimensions_labels(cls, dataset_metadata: DatasetMetadata) -> dict[str, str | None]:
        return {dimension.code: dimension.label for dimension in dataset_metadata.dimensions}

    @classmethod
    def _build_dimensions_values_labels(cls, dataset_metadata: DatasetMetadata) -> dict[str, dict[str, str | None]]:
        return {
            dimension.code: {value.code: value.label for value in dimension.values}
            for dimension in dataset_metadata.dimensions
            if dimension.values
        }

    def _get_dimension_values_as_list(self, dimension_code: str) -> list[tuple[str, str | None]]:
        values = self.dimensions_values_labels.get(dimension_code)
        if values is None:
            return []

        if isinstance(values, dict):
            values = list(values.items())

        return values

    def _get_or_create_dimensions_codes_order(self) -> list[str]:
        if self.dimensions_codes_order is not None:
            return self.dimensions_codes_order

        return sorted(set(self.dimensions_labels.keys()) | set(dict(self.dimensions_values_labels).keys()))

    def _iter_attributes_as_domain_model(self) -> Iterator[Attribute]:
        for attribute_code in self.attribute_codes:
            label = self.attributes_labels.get(attribute_code)
            values = [
                AttributeValue.create(value_code, label=value_label)
                for value_code, value_label in self.attributes_values_labels.get(attribute_code, {}).items()
            ]
            yield Attribute.create(attribute_code, label=label, values=values)

    def _iter_dimensions_as_domain_model(self) -> Iterator[Dimension]:
        for dimension_code in self._get_or_create_dimensions_codes_order():
            label = self.dimensions_labels.get(dimension_code)
            values = list(self._iter_dimension_values_as_domain_model(dimension_code))
            yield Dimension.create(dimension_code, label=label, values=values)

    def _iter_dimension_values_as_domain_model(self, dimension_code: str) -> Iterator[DimensionValue]:
        for value_code, value_label in self._get_dimension_values_as_list(dimension_code):
            try:
                yield DimensionValue.create(value_code, label=value_label)
            except SimpleCodeParseError as exc:
                raise DimensionValueCreateError(
                    dataset_json=self, dimension_code=dimension_code, dimension_value_code=value_code
                ) from exc
