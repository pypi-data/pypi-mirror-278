from collections.abc import Iterator, Mapping, Sequence
from dataclasses import dataclass, field, fields, is_dataclass
from typing import TYPE_CHECKING, Any, Protocol, TypeVar, cast, runtime_checkable

from dbnomics_data_model.diff_utils.data_change import DataChange
from dbnomics_data_model.diff_utils.data_patch import DataPatch
from dbnomics_data_model.diff_utils.sentinels import MISSING, Missing
from dbnomics_data_model.diff_utils.types import ChangePath, ChangeType

if TYPE_CHECKING:
    from _typeshed import DataclassInstance


@runtime_checkable
class MatchableItem(Protocol):
    @property
    def __match_key__(self) -> Any: ...


D = TypeVar("D", bound="DataclassInstance")
M = TypeVar("M", bound=MatchableItem)
T = TypeVar("T")


@dataclass(kw_only=True)
class DataDiffer:
    base_path: ChangePath = field(default_factory=list)

    def diff(self, old_value: T | None, new_value: T | None) -> "DataPatch":
        return DataPatch(changes=list(self.iter_changes(old_value, new_value)))

    def iter_changes(self, old_value: T | None, new_value: T | None) -> "Iterator[DataChange]":
        if old_value == new_value:
            return

        if old_value is None and new_value is not None:
            # Addition
            yield DataChange(
                change_path=self.base_path,
                change_type=ChangeType.ADD,
                new_value=new_value,
                old_value=MISSING,
            )
            return

        if old_value is not None and new_value is None:
            # Deletion
            yield DataChange(
                change_path=self.base_path,
                change_type=ChangeType.DELETE,
                new_value=MISSING,
                old_value=old_value,
            )
            return

        assert old_value is not None
        assert new_value is not None

        if type(old_value) != type(new_value):
            msg = f"old_value and new_value must have the same type, got {(type(old_value).__name__, type(new_value).__name__)}"  # noqa: E501
            raise RuntimeError(msg)

        if isinstance(old_value, float | str) and isinstance(new_value, float | str):
            yield from self._iter_scalar_changes(old_value, new_value)

        elif is_dataclass(old_value) and is_dataclass(new_value):
            yield from self._iter_dataclass_changes(
                cast("DataclassInstance", old_value),
                cast("DataclassInstance", new_value),
            )

        elif isinstance(old_value, Mapping) and isinstance(new_value, Mapping):
            yield from self._iter_mapping_changes(old_value, new_value)

        elif isinstance(old_value, Sequence) and isinstance(new_value, Sequence):
            yield from self._iter_sequence_changes(old_value, new_value)

        else:
            raise NotImplementedError((type(old_value), type(new_value)))

    def _iter_dataclass_changes(self, old_instance: D, new_instance: D) -> "Iterator[DataChange]":
        for instance_field in fields(new_instance):
            field_name = instance_field.name
            old_field_value = getattr(old_instance, field_name)
            new_field_value = getattr(new_instance, field_name)
            differ = DataDiffer(base_path=[*self.base_path, field_name])
            yield from differ.iter_changes(old_field_value, new_field_value)

    def _iter_mapping_changes(self, old_items: Mapping[str, M], new_items: Mapping[str, M]) -> "Iterator[DataChange]":
        raise NotImplementedError((old_items, new_items))

    def _iter_sequence_changes(self, old_items: Sequence[M], new_items: Sequence[M]) -> "Iterator[DataChange]":
        old_index = {item.__match_key__: (index, item) for index, item in enumerate(old_items)}
        new_index = {item.__match_key__: (index, item) for index, item in enumerate(new_items)}

        for key in sorted(old_index.keys() | new_index.keys()):
            new_value_tuple = new_index.get(key, MISSING)
            old_value_tuple = old_index.get(key, MISSING)

            if not isinstance(new_value_tuple, Missing) and not isinstance(old_value_tuple, Missing):
                new_value_index, new_value = new_value_tuple
                old_value_index, old_value = old_value_tuple
                if new_value != old_value:
                    differ = DataDiffer(
                        base_path=[
                            *self.base_path,
                            (old_value_index, new_value_index)
                            if old_value_index != new_value_index
                            else f"{new_value_index}({key})",
                        ]
                    )
                    yield from differ.iter_changes(old_value, new_value)

            elif not isinstance(old_value_tuple, Missing):
                old_value_index, old_value = old_value_tuple
                yield DataChange(
                    change_path=[*self.base_path, old_value_index],
                    change_type=ChangeType.DELETE,
                    new_value=MISSING,
                    old_value=old_value,
                )

            elif not isinstance(new_value_tuple, Missing):
                new_value_index, new_value = new_value_tuple
                yield DataChange(
                    change_path=[*self.base_path, new_value_index],
                    change_type=ChangeType.ADD,
                    new_value=new_value,
                    old_value=MISSING,
                )

            else:
                raise NotImplementedError(key)

    def _iter_scalar_changes(self, old_value: T, new_value: T) -> "Iterator[DataChange]":
        yield DataChange(
            change_path=self.base_path, change_type=ChangeType.MODIFY, new_value=new_value, old_value=old_value
        )
