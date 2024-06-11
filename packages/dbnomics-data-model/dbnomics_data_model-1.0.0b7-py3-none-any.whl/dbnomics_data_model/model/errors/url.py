from dbnomics_data_model.errors import DataModelError


class PublicUrlParseError(DataModelError):
    def __init__(self, *, value: str) -> None:
        msg = f"Could not parse a public URL from string {value!r}"
        super().__init__(msg=msg)
        self.value = value


class UrlParseError(DataModelError):
    def __init__(self, *, value: str) -> None:
        msg = f"Could not parse an URL from string {value!r}"
        super().__init__(msg=msg)
        self.value = value
