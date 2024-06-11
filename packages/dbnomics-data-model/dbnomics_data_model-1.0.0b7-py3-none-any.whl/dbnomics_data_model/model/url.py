from functools import partial
from typing import Self

import validators
from phantom import Phantom

from dbnomics_data_model.model.errors.url import PublicUrlParseError, UrlParseError

__all__ = ["PublicUrl", "Url"]


def is_url(value: str, *, simple_host: bool) -> bool:
    result = validators.url(value, simple_host=simple_host)
    if not result:
        raise result
    return True


class PublicUrl(str, Phantom[str], predicate=partial(is_url, simple_host=False)):
    __slots__ = ()

    @classmethod
    def parse(cls, value: str) -> Self:  # type: ignore[override]
        try:
            return super().parse(value)
        except TypeError as exc:
            raise PublicUrlParseError(value=value) from exc


class Url(str, Phantom[str], predicate=partial(is_url, simple_host=True)):
    __slots__ = ()

    @classmethod
    def parse(cls, value: str) -> Self:  # type: ignore[override]
        try:
            return super().parse(value)
        except TypeError as exc:
            raise UrlParseError(value=value) from exc
