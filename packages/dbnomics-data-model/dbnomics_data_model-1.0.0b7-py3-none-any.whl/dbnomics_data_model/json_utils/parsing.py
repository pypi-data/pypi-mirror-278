from pathlib import Path
from typing import Any, TypeVar, cast

import cysimdjson
from jsonalias import Json
from typedload.dataloader import Loader
from typedload.exceptions import TypedloadException

from dbnomics_data_model.json_utils.types import JsonObject

from .errors import JsonBytesParseError, JsonFileParseError, JsonParseTypeError

__all__ = ["default_json_parser", "parse_json_bytes", "parse_json_bytes_as_object", "parse_json_data"]


T = TypeVar("T")


default_json_parser = cysimdjson.JSONParser()
default_loader = Loader()


def parse_json_bytes(value: bytes) -> Json:
    try:
        return cast(Json, default_json_parser.parse(value))
    except ValueError as exc:
        raise JsonBytesParseError(value=value) from exc


def parse_json_bytes_as_object(value: bytes) -> JsonObject:
    try:
        data = default_json_parser.parse(value)
    except ValueError as exc:
        raise JsonBytesParseError(value=value) from exc

    if not isinstance(data, cysimdjson.JSONObject):
        raise JsonParseTypeError(data=cast(Json, data), expected_type=dict)

    return cast(JsonObject, data)


def parse_json_data(data: Any, *, loader: Loader | None = None, type_: type[T]) -> T:
    if loader is None:
        loader = default_loader

    try:
        return loader.load(data, type_=type_)
    except TypedloadException as exc:
        raise JsonParseTypeError(data=data, expected_type=type_) from exc


def parse_json_file(file: Path) -> Json:
    try:
        return cast(Json, default_json_parser.load(str(file)))
    except OSError as exc:
        # cysimdjson does not raise a FileNotFoundError
        if not file.is_file():
            raise FileNotFoundError from exc
    except ValueError as exc:
        raise JsonFileParseError(file_path=file) from exc
