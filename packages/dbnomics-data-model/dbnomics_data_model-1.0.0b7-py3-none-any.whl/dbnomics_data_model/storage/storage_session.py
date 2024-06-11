from abc import ABC, abstractmethod
from types import TracebackType
from typing import TYPE_CHECKING, Self

from dbnomics_data_model.storage.errors.storage_session import StorageSessionAlreadyEntered

if TYPE_CHECKING:
    from dbnomics_data_model.storage.storage import Storage


__all__ = ["StorageSession"]


class StorageSession(ABC):
    def __init__(self, name: str, *, storage: "Storage") -> None:
        self.name = name
        self.storage = storage
        self._has_committed = False
        self._has_entered = False

    def __enter__(self) -> Self:
        if self._has_entered:
            raise StorageSessionAlreadyEntered(storage_session=self)
        self._has_entered = True
        return self

    def __exit__(
        self, exc_type: type[BaseException] | None, exc: BaseException | None, traceback: TracebackType | None
    ) -> None:
        if not self._has_committed:
            # Always rollback whether or not there was an exception to force the caller to commit explicitly
            # before exiting the context manager.
            self.rollback()

    def commit(self) -> None:
        self._has_committed = True

    @abstractmethod
    def rollback(self) -> None:
        pass
