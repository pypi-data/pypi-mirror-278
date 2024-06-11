from collections.abc import Callable, Iterable, Iterator
from typing import Any, TypeVar

T = TypeVar("T")


def iter_merged_items(
    *,
    key: Callable[[T], Any],
    merge: Callable[[T, T], T],
    source: Iterable[T],
    target: Iterable[T],
) -> Iterator[T]:
    """Yield `target` items merged with `source` items if they exist, then yield `source`-only items.

    The `key` function matches items between `source` and `target`.

    The `merge` merges items.
    """
    source_item_by_key = {key(source_item): source_item for source_item in source}

    for target_item in target:
        target_item_key = key(target_item)
        source_item = source_item_by_key.get(target_item_key)
        if source_item is None:
            yield target_item
        else:
            yield merge(target_item, source_item)


def merge_iterables_of_items(
    *,
    key: Callable[[T], Any],
    merge: Callable[[T, T], T],
    sort_by_key: bool = False,
    source: Iterable[T],
    target: Iterable[T],
) -> list[T]:
    merged_items_iter = iter_merged_items(key=key, merge=merge, source=source, target=target)
    return sorted(merged_items_iter, key=key) if sort_by_key else list(merged_items_iter)
