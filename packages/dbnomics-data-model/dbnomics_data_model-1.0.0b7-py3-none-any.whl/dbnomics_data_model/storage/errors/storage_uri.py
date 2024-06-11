from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from dbnomics_data_model.errors import DataModelError
from dbnomics_data_model.utils import get_function_name

if TYPE_CHECKING:
    from dbnomics_data_model.storage.storage_uri import StorageUri, StorageUriScheme


class StorageUriParamValueParseError(DataModelError):
    def __init__(
        self,
        *,
        param_name: str,
        param_value_str: str,
        parse: Callable[[str], Any],
        valid_values: list[str] | None = None,
    ) -> None:
        msg = f"Error parsing the value {param_value_str!r} of the URI parameter {param_name!r}"

        function_name = get_function_name(parse)
        if function_name is not None:
            msg += f" with the function {function_name!r}"

        if valid_values is not None:
            msg += f", valid values: {', '.join(valid_values)}"

        super().__init__(msg=msg)

        self.param_name = param_name
        self.param_value = param_value_str
        self.parse = parse
        self.valid_values = valid_values


class StorageUriError(DataModelError):
    def __init__(self, *, msg: str, uri: "StorageUri") -> None:
        super().__init__(msg=msg)
        self.uri = uri


class StorageUriParseError(DataModelError):
    def __init__(self, *, msg: str, uri: str) -> None:
        super().__init__(msg=msg)
        self.uri = uri


class StorageUriMissingScheme(StorageUriParseError):
    def __init__(self, *, uri: str) -> None:
        msg = f"Scheme is required in the URI {uri!r}"
        super().__init__(uri=uri, msg=msg)


class StorageUriPathParseError(StorageUriParseError):
    def __init__(self, *, path: str, uri: str) -> None:
        msg = f"Error parsing the path {path!r} of the URI {uri!r}"
        super().__init__(uri=uri, msg=msg)
        self.path = path


class StorageUriQueryParseError(StorageUriParseError):
    def __init__(self, *, query: str, uri: str) -> None:
        msg = f"Error parsing the query {query!r} of the URI {uri!r}"
        super().__init__(uri=uri, msg=msg)
        self.query = query


class StorageUriSchemeParseError(StorageUriParseError):
    def __init__(self, *, scheme: str, uri: str, valid_values: list[str]) -> None:
        msg = f"Error parsing the scheme {scheme!r} of the URI {uri!r}, valid values: {', '.join(valid_values)}"
        super().__init__(uri=uri, msg=msg)
        self.scheme = scheme
        self.valid_values = valid_values


class StorageUriUrlParseError(StorageUriParseError):
    def __init__(self, *, uri: str) -> None:
        msg = f"Error parsing the URI {uri!r} as an URL"
        super().__init__(uri=uri, msg=msg)


class UnsupportedStorageUriScheme(DataModelError):
    def __init__(self, *, scheme: "StorageUriScheme") -> None:
        msg = f"Unsupported storage URI scheme {scheme.value!r}"
        super().__init__(msg=msg)
