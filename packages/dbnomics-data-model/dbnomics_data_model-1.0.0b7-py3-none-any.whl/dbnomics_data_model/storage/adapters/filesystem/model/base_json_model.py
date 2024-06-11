from dataclasses import dataclass
from typing import Self, cast

from jsonalias import Json
from typedload.datadumper import Dumper
from typedload.dataloader import Loader

from dbnomics_data_model.json_utils.dumping import dump_as_json_data
from dbnomics_data_model.json_utils.errors import JsonDumpError, JsonParseTypeError
from dbnomics_data_model.json_utils.parsing import parse_json_data
from dbnomics_data_model.json_utils.types import JsonObject
from dbnomics_data_model.storage.adapters.filesystem.errors.json_model import JsonModelDumpError, JsonModelParseError


def create_dumper() -> Dumper:
    return Dumper(hidedefault=False, isodates=True)


def create_loader() -> Loader:
    return Loader(
        dictequivalence=False,  # for compatibility with cysimdjson.JSONObject
    )


loader = create_loader()
dumper = create_dumper()


@dataclass
class BaseJsonObjectModel:
    @classmethod
    def from_json_data(cls, data: Json) -> Self:
        try:
            return parse_json_data(data, loader=loader, type_=cls)
        except JsonParseTypeError as exc:
            raise JsonModelParseError(data=data) from exc

    def to_json_data(self) -> JsonObject:
        try:
            data = dump_as_json_data(self, dumper=dumper)
        except JsonDumpError as exc:
            raise JsonModelDumpError(obj=self) from exc
        return cast(JsonObject, data)
