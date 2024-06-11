from enum import Enum

__all__ = ["StorageVariant"]


class StorageVariant(Enum):
    JSON_LINES = "jsonl"
    TSV = "tsv"
