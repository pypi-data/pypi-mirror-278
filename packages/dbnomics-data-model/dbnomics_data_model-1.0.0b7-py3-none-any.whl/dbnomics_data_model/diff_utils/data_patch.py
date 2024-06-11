from collections.abc import Sequence
from dataclasses import dataclass

from dbnomics_data_model.diff_utils.data_change import DataChange


@dataclass(frozen=True, kw_only=True)
class DataPatch:
    changes: Sequence[DataChange]
