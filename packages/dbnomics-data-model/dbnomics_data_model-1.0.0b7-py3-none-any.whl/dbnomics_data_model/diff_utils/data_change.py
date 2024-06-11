from dataclasses import dataclass
from typing import Any

from dbnomics_data_model.diff_utils.sentinels import Missing
from dbnomics_data_model.diff_utils.types import ChangePath, ChangeType


@dataclass(frozen=True, kw_only=True)
class DataChange:
    change_path: ChangePath
    change_type: ChangeType
    new_value: Any | Missing
    old_value: Any | Missing
