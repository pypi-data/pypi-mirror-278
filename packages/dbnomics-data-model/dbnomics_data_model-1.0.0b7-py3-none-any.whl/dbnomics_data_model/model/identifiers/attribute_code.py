import re
from typing import Final, Self

from phantom import Phantom

from dbnomics_data_model.model.constants import PERIOD, VALUE
from dbnomics_data_model.model.identifiers.errors import AttributeCodeParseError

__all__ = ["AttributeCode"]


attribute_code_re: Final = re.compile(r"[-0-9A-Za-z._ ]+")

forbidden_attribute_codes: Final = [PERIOD, VALUE]


def is_attribute_code(value: str) -> bool:
    match = re.fullmatch(attribute_code_re, value)
    if match is None:
        return False
    return value not in forbidden_attribute_codes


class AttributeCode(str, Phantom[str], predicate=is_attribute_code):
    __slots__ = ()

    @classmethod
    def parse(cls, value: str) -> Self:  # type: ignore[override]
        try:
            return super().parse(value)
        except TypeError as exc:
            raise AttributeCodeParseError(value=value) from exc
