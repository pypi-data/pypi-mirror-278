from typing import Literal

import daiquiri

from dbnomics_data_model.model.dimensions.dataset_dimensions import DatasetDimensions
from dbnomics_data_model.model.dimensions.dimension import Dimension
from dbnomics_data_model.model.dimensions.dimension_value import DimensionValue
from dbnomics_data_model.model.frequency import Frequency
from dbnomics_data_model.model.identifiers.types import DimensionCode, DimensionValueCode

__all__ = ["add_missing_dataset_dimensions"]


logger = daiquiri.getLogger(__name__)


def add_missing_dataset_dimensions(
    dataset_dimensions: DatasetDimensions,
    *,
    dimension_codes: set[DimensionCode] | Literal[True],
    dimensions: dict[DimensionCode, DimensionValueCode],
) -> None:
    frequency_dimension_code = dataset_dimensions.frequency_dimension_code

    dimension_codes = set(dimensions.keys()) if dimension_codes is True else dimension_codes
    for dimension_code in dimension_codes:
        dimension = dataset_dimensions.find_dimension_by_code(dimension_code)

        if dimension is None:
            dimension = Dimension(code=dimension_code)
            logger.debug("Adding missing dimension %r to dataset", dimension_code)
            dataset_dimensions.dimensions.append(dimension)

        dimension_value_code = dimensions.get(dimension_code)
        if dimension_value_code is None:
            msg = f"No value is defined for dimension {dimension_code!r} for that series"
            raise RuntimeError(msg)

        dimension_value = dimension.find_value_by_code(dimension_value_code)
        if dimension_value is None:
            is_frequency_dimension = frequency_dimension_code is not None and dimension_code == frequency_dimension_code
            dimension_value_label = None
            if is_frequency_dimension:
                dimension_value_label = Frequency.parse_code(dimension_value_code).value.label
            dimension_value = DimensionValue(code=dimension_value_code, label=dimension_value_label)
            logger.debug("Adding missing value %r to dimension %r of dataset", dimension_value.code, dimension.code)
            dimension.values.append(dimension_value)
