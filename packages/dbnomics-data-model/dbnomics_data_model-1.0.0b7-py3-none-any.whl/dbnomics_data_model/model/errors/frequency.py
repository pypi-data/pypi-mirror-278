from dbnomics_data_model.errors import DataModelError


class InvalidFrequencyCode(DataModelError):
    def __init__(self, *, value: str) -> None:
        msg = f"Invalid frequency code: {value!r}"
        super().__init__(msg=msg)
        self.value = value
