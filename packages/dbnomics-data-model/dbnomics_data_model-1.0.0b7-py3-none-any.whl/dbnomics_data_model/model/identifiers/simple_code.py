import re
from typing import Final, Self

from phantom.re import FullMatch

from dbnomics_data_model.model.identifiers.errors import SimpleCodeParseError

__all__ = ["SimpleCode"]


simple_code_re: Final = re.compile(r"[-0-9A-Za-z._]+")


class SimpleCode(FullMatch, pattern=simple_code_re):
    __slots__ = ()

    @classmethod
    def parse(cls, value: str) -> Self:  # type: ignore[override]
        try:
            return super().parse(value)
        except TypeError as exc:
            raise SimpleCodeParseError(value=value) from exc
