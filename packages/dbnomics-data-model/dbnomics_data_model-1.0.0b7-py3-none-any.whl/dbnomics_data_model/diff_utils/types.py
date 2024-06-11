from collections.abc import Sequence
from enum import Enum
from typing import TypeAlias

ChangePath: TypeAlias = Sequence[int | tuple[int, int] | str]


class ChangeType(Enum):
    ADD = "A"
    DELETE = "D"
    MODIFY = "M"


FieldName: TypeAlias = str
