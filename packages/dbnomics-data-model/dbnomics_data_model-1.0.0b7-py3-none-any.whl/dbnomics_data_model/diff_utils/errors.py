from typing import TYPE_CHECKING

from dbnomics_data_model.errors import DataModelError

if TYPE_CHECKING:
    from _typeshed import DataclassInstance


class DataclassDiffError(DataModelError):
    def __init__(self, *, msg: str, source: "DataclassInstance", target: "DataclassInstance") -> None:
        super().__init__(msg=msg)
        self.source = source
        self.target = target


class DataclassFieldsMismatch(DataclassDiffError):
    def __init__(self, *, old_instance: "DataclassInstance", new_instance: "DataclassInstance") -> None:
        msg = "Source and target dataclasses must have the same fields"
        super().__init__(msg=msg, source=old_instance, target=new_instance)
