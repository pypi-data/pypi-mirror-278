from dbnomics_data_model.errors import DataModelError


class IdentifierParseError(DataModelError):
    def __init__(self, *, msg: str, value: str) -> None:
        super().__init__(msg=msg)
        self.value = value


class AttributeCodeParseError(IdentifierParseError):
    def __init__(self, *, value: str) -> None:
        msg = f"Could not parse an attribute code from string {value!r}"
        super().__init__(msg=msg, value=value)


class BareDatasetIdParseError(IdentifierParseError):
    def __init__(self, *, value: str) -> None:
        msg = f"Could not parse a bare dataset ID from string {value!r}"
        super().__init__(msg=msg, value=value)


class DatasetCodeParseError(IdentifierParseError):
    def __init__(self, *, value: str) -> None:
        msg = f"Could not parse a dataset code from string {value!r}"
        super().__init__(msg=msg, value=value)


class DatasetIdParseError(IdentifierParseError):
    def __init__(self, *, value: str) -> None:
        msg = f"Could not parse a dataset ID from string {value!r}"
        super().__init__(msg=msg, value=value)


class ResolvableDatasetCodeParseError(IdentifierParseError):
    def __init__(self, *, value: str) -> None:
        msg = f"Could not parse a resolvable dataset code from string {value!r}"
        super().__init__(msg=msg, value=value)


class ResolvableDatasetIdParseError(IdentifierParseError):
    def __init__(self, *, value: str) -> None:
        msg = f"Could not parse a resolvable dataset ID from string {value!r}"
        super().__init__(msg=msg, value=value)


class SeriesCodeParseError(IdentifierParseError):
    def __init__(self, *, value: str) -> None:
        msg = f"Could not parse a series code from string {value!r}"
        super().__init__(msg=msg, value=value)


class SeriesIdParseError(IdentifierParseError):
    def __init__(self, *, value: str) -> None:
        msg = f"Could not parse a series ID from string {value!r}"
        super().__init__(msg=msg, value=value)


class SimpleCodeParseError(IdentifierParseError):
    def __init__(self, *, value: str) -> None:
        msg = f"Could not parse a simple code from string {value!r}"
        super().__init__(msg=msg, value=value)
