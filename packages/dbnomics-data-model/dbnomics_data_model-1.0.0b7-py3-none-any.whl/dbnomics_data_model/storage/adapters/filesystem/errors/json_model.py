from typing import TYPE_CHECKING

from jsonalias import Json

from dbnomics_data_model.storage.adapters.filesystem.errors import FileSystemAdapterError

if TYPE_CHECKING:
    from dbnomics_data_model.storage.adapters.filesystem.model.base_json_model import BaseJsonObjectModel


class JsonModelError(FileSystemAdapterError):
    pass


class JsonModelDumpError(JsonModelError):
    def __init__(self, *, obj: "BaseJsonObjectModel") -> None:
        msg = "Could not dump JSON model instance as JSON data"
        super().__init__(msg=msg)
        self.obj = obj


class JsonModelParseError(JsonModelError):
    def __init__(self, *, data: Json) -> None:
        msg = "Could not initialize JSON model instance from JSON data"
        super().__init__(msg=msg)
        self.data = data
