from typing import Any

import orjson

from .errors import JsonDataSerializeError

__all__ = ["serialize_json", "serialize_json_line"]


def serialize_json(
    data: Any,  # could be a dataclass, which jsonalias.Json does not cover
) -> bytes:
    """Serialize JSONable data to a multi-line byte string.

    Data is indented and keys are sorted.
    """
    try:
        return orjson.dumps(data, option=orjson.OPT_INDENT_2 | orjson.OPT_SORT_KEYS)
    except orjson.JSONEncodeError as exc:
        raise JsonDataSerializeError(data=data) from exc


def serialize_json_line(
    data: Any,  # could be a dataclass, which jsonalias.Json does not cover
) -> bytes:
    """Serialize JSONable data to a single-line byte string.

    This is useful to produce a JSON lines file.

    Raise a JsonSerializeError if JSON data could not be serialized.
    """
    try:
        return orjson.dumps(data, option=orjson.OPT_SORT_KEYS)
    except orjson.JSONEncodeError as exc:
        raise JsonDataSerializeError(data=data) from exc
