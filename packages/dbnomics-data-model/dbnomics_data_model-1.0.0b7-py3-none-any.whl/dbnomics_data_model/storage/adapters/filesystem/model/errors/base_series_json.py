from typing import TYPE_CHECKING

from dbnomics_data_model.storage.adapters.filesystem.errors.json_model import JsonModelError

if TYPE_CHECKING:
    from dbnomics_data_model.storage.adapters.filesystem.model.base_series_json import BaseSeriesJson


class SeriesJsonError(JsonModelError):
    def __init__(self, *, series_json: "BaseSeriesJson", msg: str) -> None:
        super().__init__(msg=msg)
        self.series_json = series_json


class UnknownDimensionCodesOrder(SeriesJsonError):
    def __init__(self, *, series_json: "BaseSeriesJson") -> None:
        msg = "dimensions_codes_order must be given when dimensions is a list"
        super().__init__(series_json=series_json, msg=msg)


class InconsistentDimensions(SeriesJsonError):
    def __init__(self, *, series_json: "BaseSeriesJson") -> None:
        msg = "dimensions_codes_order and series dimensions must have the same length"
        super().__init__(series_json=series_json, msg=msg)
