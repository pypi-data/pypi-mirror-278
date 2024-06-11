from pathlib import Path
from typing import Any

from jsonalias import Json

from dbnomics_data_model.errors import DataModelError


class JsonError(DataModelError):
    pass


class JsonDumpError(JsonError):
    def __init__(self, *, value: Any) -> None:
        msg = "Could not dump value as JSON data"
        super().__init__(msg=msg)
        self.value = value


class JsonParseError(JsonError):
    pass


class JsonBytesParseError(JsonParseError):
    def __init__(self, *, value: bytes) -> None:
        msg = "Could not parse bytes as JSON data"
        super().__init__(msg=msg)
        self.value = value


class JsonFileParseError(JsonParseError):
    def __init__(self, *, file_path: Path) -> None:
        msg = f"Could not parse {str(file_path)!r} as JSON data"
        super().__init__(msg=msg)
        self.file_path = file_path


class JsonFileSaveError(JsonError):
    def __init__(self, *, data: Json, file_path: Path, serialized_data: bytes) -> None:
        msg = f"Could not write bytes to {str(file_path)!r}"
        super().__init__(msg=msg)
        self.data = data
        self.file_path = file_path
        self.serialized_data = serialized_data


class JsonLineParseError(JsonParseError):
    def __init__(self, *, file_path: Path, line: bytes) -> None:
        msg = f"Could not parse line of {str(file_path)!r} as JSON data"
        super().__init__(msg=msg)
        self.file_path = file_path
        self.line = line


class JsonParseTypeError(JsonParseError):
    def __init__(self, *, data: Json, expected_type: type) -> None:
        msg = f"Could not parse data of type {type(data)!r} as {expected_type!r}"
        super().__init__(msg=msg)
        self.data = data
        self.expected_type = expected_type


class JsonDataSerializeError(JsonError):
    def __init__(self, *, data: Json) -> None:
        msg = "Could not serialize JSON data as bytes"
        super().__init__(msg=msg)
        self.data = data
