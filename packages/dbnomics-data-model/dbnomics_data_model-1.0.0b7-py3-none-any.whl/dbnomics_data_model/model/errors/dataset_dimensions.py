from typing import TYPE_CHECKING

from dbnomics_data_model.errors import DataModelError

if TYPE_CHECKING:
    from dbnomics_data_model.model.dimensions.dataset_dimensions import DatasetDimensions
    from dbnomics_data_model.model.identifiers.types import DimensionCode


class DatasetDimensionsError(DataModelError):
    def __init__(self, *, dataset_dimensions: "DatasetDimensions", msg: str) -> None:
        super().__init__(msg=msg)
        self.dataset_dimensions = dataset_dimensions


class UndefinedDatasetDimension(DatasetDimensionsError):
    def __init__(self, *, dataset_dimensions: "DatasetDimensions", dimension_code: "DimensionCode") -> None:
        msg = f"{dimension_code!r} is not a dimension of this dataset"
        super().__init__(dataset_dimensions=dataset_dimensions, msg=msg)
        self.dimension_code = dimension_code
