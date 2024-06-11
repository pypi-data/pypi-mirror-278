from typing import TypeAlias

from jsonalias import Json

__all__ = ["JsonObject"]


JsonObject: TypeAlias = dict[str, Json]
