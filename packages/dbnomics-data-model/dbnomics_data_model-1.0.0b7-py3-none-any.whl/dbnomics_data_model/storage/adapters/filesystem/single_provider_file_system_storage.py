from collections.abc import Iterator
from pathlib import Path

from dbnomics_data_model.model import ProviderCode
from dbnomics_data_model.storage.adapters.filesystem.file_system_storage import FileSystemStorage

__all__ = ["SingleProviderFileSystemStorage"]


class SingleProviderFileSystemStorage(FileSystemStorage):
    def clone(self, *, storage_dir: Path) -> "SingleProviderFileSystemStorage":
        return SingleProviderFileSystemStorage(
            auto_create=self.auto_create,
            default_storage_variant=self.default_storage_variant,
            series_offset_repo=self._series_offset_repo,
            storage_dir=storage_dir,
        )

    def delete_provider_dir(self, provider_code: ProviderCode, *, missing_ok: bool = False) -> None:  # noqa: ARG002
        msg = "delete_provider_dir is a forbidden method with SingleProviderFileSystemStorage"
        raise NotImplementedError(msg)

    def get_provider_dir(self, provider_code: ProviderCode) -> Path:  # noqa: ARG002
        return self.storage_dir

    def iter_provider_directories(self) -> Iterator[Path]:
        yield self.storage_dir
