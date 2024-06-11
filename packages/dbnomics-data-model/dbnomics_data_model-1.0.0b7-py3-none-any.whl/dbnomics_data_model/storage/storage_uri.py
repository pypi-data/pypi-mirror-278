from abc import ABC
from collections.abc import Callable
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Final, TypeVar
from urllib.parse import parse_qsl, urlencode, urlparse

import daiquiri

from dbnomics_data_model.storage.errors.storage_uri import (
    StorageUriMissingScheme,
    StorageUriParamValueParseError,
    StorageUriPathParseError,
    StorageUriQueryParseError,
    StorageUriSchemeParseError,
    StorageUriUrlParseError,
    UnsupportedStorageUriScheme,
)
from dbnomics_data_model.utils import get_enum_values

__all__ = ["StorageUri", "parse_storage_uri"]


T = TypeVar("T")

logger = daiquiri.getLogger(__name__)


AUTO_CREATE_DEFAULT_VALUE: Final = True


class StorageUriParam(Enum):
    AUTO_CREATE = "auto_create"


@dataclass(frozen=True, kw_only=True)
class StorageUriParams:
    auto_create: bool = AUTO_CREATE_DEFAULT_VALUE

    def __str__(self) -> str:
        return urlencode(sorted(asdict(self).items()))


class StorageUriScheme(Enum):
    FILESYSTEM = "filesystem"


@dataclass(frozen=True, kw_only=True)
class StorageUri(ABC):
    params: StorageUriParams = field(default_factory=StorageUriParams)
    path: Path
    scheme: StorageUriScheme

    @classmethod
    def parse(cls, uri: str) -> "StorageUri":
        uri_components = parse_storage_uri_components(uri)
        if uri_components.scheme == StorageUriScheme.FILESYSTEM:
            from dbnomics_data_model.storage.adapters.filesystem.file_system_storage_uri import FileSystemStorageUri

            return FileSystemStorageUri.create(params_data=uri_components.params_data, path=uri_components.path)

        raise UnsupportedStorageUriScheme(scheme=uri_components.scheme)

    def __str__(self) -> str:
        path_str = "" if self.path is None else self.path
        storage_uri_str = f"{self.scheme.value}:{path_str}"
        params_str = str(self.params)
        if params_str:
            storage_uri_str += f"?{params_str}"
        return storage_uri_str


@dataclass(frozen=True, kw_only=True)
class StorageUriComponents:
    params_data: dict[str, str]
    path: Path
    scheme: StorageUriScheme


def parse_storage_uri(storage_uri_or_dir: Path | str) -> StorageUri:
    if isinstance(storage_uri_or_dir, Path):
        return parse_storage_uri_from_dir(storage_uri_or_dir)

    try:
        return StorageUri.parse(storage_uri_or_dir)
    except StorageUriMissingScheme:
        logger.debug(
            "Could not find a scheme in storage URI %r, falling back considering it's a directory",
            storage_uri_or_dir,
        )

        try:
            storage_dir = Path(storage_uri_or_dir)
        except Exception as exc:
            msg = f"{storage_uri_or_dir!r} is not a valid storage URI or directory"
            raise ValueError(msg) from exc

    return parse_storage_uri_from_dir(storage_dir)


def parse_storage_uri_components(uri: str) -> StorageUriComponents:
    try:
        parsed = urlparse(uri)
    except Exception as exc:
        raise StorageUriUrlParseError(uri=uri) from exc

    scheme_str = parsed.scheme
    if not scheme_str:
        raise StorageUriMissingScheme(uri=uri)
    try:
        scheme = StorageUriScheme(scheme_str)
    except ValueError as exc:
        raise StorageUriSchemeParseError(
            scheme=scheme_str, uri=uri, valid_values=get_enum_values(StorageUriScheme)
        ) from exc

    try:
        path = Path(parsed.path)
    except Exception as exc:
        raise StorageUriPathParseError(uri=uri, path=parsed.path) from exc

    try:
        params_data = dict(parse_qsl(parsed.query, strict_parsing=True))
    except Exception as exc:
        raise StorageUriQueryParseError(uri=uri, query=parsed.query) from exc

    return StorageUriComponents(params_data=params_data, path=path, scheme=scheme)


def parse_storage_uri_from_dir(storage_dir: Path) -> StorageUri:
    from dbnomics_data_model.storage.adapters.filesystem.file_system_storage_uri import (
        FileSystemStorageUri,
        FileSystemStorageUriParams,
    )

    params = FileSystemStorageUriParams(single_provider=True)
    return FileSystemStorageUri(params=params, path=storage_dir)


def parse_storage_uri_param(
    *,
    default: T,
    params_data: dict[str, str],
    param_name: str,
    parse: Callable[[str], T],
    valid_values: list[str] | None = None,
) -> T:
    param_value_str = params_data.get(param_name)
    if param_value_str is None:
        return default
    try:
        return parse(param_value_str)
    except Exception as exc:
        raise StorageUriParamValueParseError(
            parse=parse, param_name=param_name, param_value_str=param_value_str, valid_values=valid_values
        ) from exc
