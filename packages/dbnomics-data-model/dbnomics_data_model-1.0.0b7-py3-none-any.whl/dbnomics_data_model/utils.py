from collections.abc import Callable, Iterable
from enum import Enum
from typing import Any, TypeVar

from dbnomics_data_model.errors.utils import InvalidBoolValue

T = TypeVar("T")


def find(predicate: Callable[[T], bool], items: Iterable[T], default: T | None = None) -> T | None:
    """Find the first item in ``items`` satisfying ``predicate(item)``.

    Return the found item, or return ``default`` if no item was found.

    >>> find(lambda item: item > 2, [1, 2, 3, 4])
    3
    >>> find(lambda item: item > 10, [1, 2, 3, 4])
    >>> find(lambda item: item > 10, [1, 2, 3, 4], default=42)
    42
    """
    for item in items:
        if predicate(item):
            return item
    return default


def find_index_of_first_difference(items1: Iterable[T], items2: Iterable[T]) -> int | None:
    for index, (item1, item2) in enumerate(zip(items1, items2, strict=True)):
        if item1 != item2:
            return index

    return None


def find_index(predicate: Callable[[T], bool], items: Iterable[T], default: int | None = None) -> int | None:
    """Find the index of the first item satisfying the predicate."""
    return next((i for i, item in enumerate(items) if predicate(item)), default)


def get_enum_values(enum: type[Enum]) -> list[str]:
    return [item.value for item in list(enum)]


def get_function_name(f: Callable[..., Any]) -> str | None:
    dummy_lambda = lambda: 0  # noqa: E731

    if f.__name__ == dummy_lambda.__name__:
        return None

    return f.__qualname__


def parse_bool(value: str) -> bool:
    value_lower = value.lower()
    if value_lower in {"true", "1"}:
        return True
    if value_lower in {"false", "0"}:
        return False
    raise InvalidBoolValue(value=value)


def raise_first_error(errors: Iterable[BaseException]) -> None:
    for error in errors:
        raise error
