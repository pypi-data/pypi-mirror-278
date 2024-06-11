from typing import Any

from dbnomics_data_model.errors import DataModelError


class MergeItemsMismatch(DataModelError):
    def __init__(self, *, source: Any, target: Any) -> None:
        msg = "Source and target do not match"
        super().__init__(msg=msg)
        self.source = source
        self.target = target
