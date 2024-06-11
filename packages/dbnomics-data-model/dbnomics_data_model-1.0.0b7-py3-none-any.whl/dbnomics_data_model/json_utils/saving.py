from collections.abc import Iterable
from pathlib import Path
from typing import Any

from dbnomics_data_model.json_utils.serializing import serialize_json, serialize_json_line
from dbnomics_data_model.json_utils.types import JsonObject

from .errors import JsonFileSaveError

__all__ = ["save_json_file", "save_jsonl_file"]


def save_json_file(file_path: Path, data: Any) -> None:
    """Save a JSON file to path."""
    data_bytes = serialize_json(data)
    try:
        file_path.write_bytes(data_bytes)
    except Exception as exc:
        raise JsonFileSaveError(data=data, file_path=file_path, serialized_data=data_bytes) from exc


def save_jsonl_file(file_path: Path, items: Iterable[JsonObject], *, append_mode: bool = False) -> None:
    """Save items to a JSON Lines file."""
    mode = "ab" if append_mode else "wb"
    with file_path.open(mode) as fp:
        for item in items:
            item_bytes = serialize_json_line(item)
            try:
                fp.write(item_bytes)
                fp.write(b"\n")
            except Exception as exc:
                raise JsonFileSaveError(data=item, file_path=file_path, serialized_data=item_bytes) from exc
