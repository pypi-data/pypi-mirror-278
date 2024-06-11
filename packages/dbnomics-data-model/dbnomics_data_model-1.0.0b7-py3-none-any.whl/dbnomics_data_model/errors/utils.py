from dbnomics_data_model.errors import DataModelError


class InvalidBoolValue(DataModelError):
    def __init__(self, *, value: str) -> None:
        msg = f"String value could not be interpreted as bool: {value!r}"
        super().__init__(msg=msg)
        self.value = value
