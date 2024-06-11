from typing import TYPE_CHECKING

from dbnomics_data_model.errors import DataModelError

if TYPE_CHECKING:
    from dbnomics_data_model.storage.storage_session import StorageSession


class StorageSessionError(DataModelError):
    def __init__(self, *, msg: str, storage_session: "StorageSession") -> None:
        super().__init__(msg=msg)
        self.storage_session = storage_session


class StorageSessionAlreadyEntered(StorageSessionError):
    def __init__(self, *, storage_session: "StorageSession") -> None:
        msg = "Storage session has already entered"
        super().__init__(msg=msg, storage_session=storage_session)


class StorageSessionNeverEntered(StorageSessionError):
    def __init__(self, *, storage_session: "StorageSession") -> None:
        msg = "Storage session never entered"
        super().__init__(msg=msg, storage_session=storage_session)
