import re
from typing import Final, Self

from phantom.re import FullMatch

from dbnomics_data_model.model.identifiers.errors import SeriesCodeParseError

__all__ = ["SeriesCode"]


series_code_re: Final = re.compile(r"[^/ ]+")


class SeriesCode(FullMatch, pattern=series_code_re):
    __slots__ = ()

    @classmethod
    def parse(cls, value: str) -> Self:  # type: ignore[override]
        try:
            return super().parse(value)
        except TypeError as exc:
            raise SeriesCodeParseError(value=value) from exc
