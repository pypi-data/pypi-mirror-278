from enum import Enum

__all__ = ["DimensionRole"]


class DimensionRole(Enum):
    """The role of a dimension.

    Some dimensions can have a specific role (e.g. the "frequency" dimension).
    As DBnomics keeps the codes of the dimensions from the data providers as-is,
    the dimension role is a way to indicate which dimension have a specific role without relying on a conventional name.
    """

    FREQUENCY = "FREQUENCY"
