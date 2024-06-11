from pathlib import Path

from dbnomics_data_model.storage.adapters.filesystem.errors import FileSystemAdapterError


class SessionDirectoryNotFound(FileSystemAdapterError):
    def __init__(self, *, session_dir: Path) -> None:
        msg = f"Could not find the session directory {str(session_dir)!r}"
        super().__init__(msg=msg)
        self.session_dir = session_dir
