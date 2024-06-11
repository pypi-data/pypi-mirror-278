import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Self

import daiquiri

from dbnomics_data_model.file_utils import write_gitignore_all
from dbnomics_data_model.storage.adapters.filesystem.constants import BASE_SESSION_DIR_NAME
from dbnomics_data_model.storage.adapters.filesystem.errors.file_system_storage import StorageDirectoryNotFound
from dbnomics_data_model.storage.adapters.filesystem.errors.file_system_storage_session import SessionDirectoryNotFound
from dbnomics_data_model.storage.adapters.filesystem.file_utils import move_children
from dbnomics_data_model.storage.errors.storage_session import StorageSessionNeverEntered
from dbnomics_data_model.storage.storage_session import StorageSession

if TYPE_CHECKING:
    from dbnomics_data_model.storage.adapters.filesystem.file_system_storage import FileSystemStorage

__all__ = ["FileSystemStorageSession"]


logger = daiquiri.getLogger(__name__)


class FileSystemStorageSession(StorageSession):
    def __init__(self, name: str, *, session_dir: Path, storage: "FileSystemStorage", storage_dir: Path) -> None:
        super().__init__(name, storage=storage)

        if not session_dir.is_dir():
            raise SessionDirectoryNotFound(session_dir=session_dir)
        self.session_dir = session_dir

        if not storage_dir.is_dir():
            raise StorageDirectoryNotFound(storage_dir=storage_dir)
        self.storage_dir = storage_dir

    @classmethod
    def from_storage(cls, storage: "FileSystemStorage", *, session_name: str | None = None) -> Self:
        if session_name is None:
            session_name = datetime.isoformat(datetime.now(tz=timezone.utc))

        storage_dir = storage.storage_dir
        session_dir = cls._create_session_dir(session_dir_name=session_name, storage_dir=storage_dir)
        session_storage = storage.clone(storage_dir=session_dir)
        return cls(session_name, session_dir=session_dir, storage=session_storage, storage_dir=storage_dir)

    def commit(self) -> None:
        super().commit()

        if not self._has_entered:
            raise StorageSessionNeverEntered(storage_session=self)

        move_children(self.session_dir, self.storage_dir, overwrite=True)
        logger.debug(
            "Committed session %r by moving files from %s to %s", self.name, self.session_dir, self.storage_dir
        )

    def rollback(self) -> None:
        pass

    @classmethod
    def _create_base_session_dir(cls, *, storage_dir: Path) -> Path:
        base_session_dir = storage_dir / BASE_SESSION_DIR_NAME
        base_session_dir.mkdir(exist_ok=True)
        write_gitignore_all(base_session_dir, exist_ok=True)
        return base_session_dir

    @classmethod
    def _create_session_dir(cls, *, session_dir_name: str, storage_dir: Path) -> Path:
        base_session_dir = cls._create_base_session_dir(storage_dir=storage_dir)

        session_dir = base_session_dir / session_dir_name
        session_dir_exists = session_dir.is_dir()
        if session_dir_exists:
            shutil.rmtree(session_dir)
        session_dir.mkdir()
        logger.debug(
            "%s session directory: %s", "Deleted then re-created" if session_dir_exists else "Created", session_dir
        )

        return session_dir
