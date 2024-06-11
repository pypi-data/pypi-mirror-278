from typing import Literal, TypeAlias

from .simple_code import SimpleCode

__all__ = [
    "AttributeValueCode",
    "BareDatasetCode",
    "CategoryCode",
    "DatasetReleaseCode",
    "DimensionCode",
    "DimensionValueCode",
    "ProviderCode",
    "ResolvableDatasetReleaseCode",
]

AttributeValueCode: TypeAlias = SimpleCode
BareDatasetCode: TypeAlias = SimpleCode
CategoryCode: TypeAlias = SimpleCode
DatasetReleaseCode: TypeAlias = SimpleCode
DimensionCode: TypeAlias = SimpleCode
DimensionValueCode: TypeAlias = SimpleCode
ProviderCode: TypeAlias = SimpleCode
ResolvableDatasetReleaseCode: TypeAlias = Literal["latest"] | DatasetReleaseCode
