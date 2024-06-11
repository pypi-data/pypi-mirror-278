__all__ = ["UpdateStrategy"]


from enum import Enum


class UpdateStrategy(Enum):
    MERGE = "merge"
    REPLACE = "replace"
