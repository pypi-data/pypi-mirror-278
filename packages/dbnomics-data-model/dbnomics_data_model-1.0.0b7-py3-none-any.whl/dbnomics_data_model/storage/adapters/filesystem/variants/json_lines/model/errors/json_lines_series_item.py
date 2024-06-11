from typing import TYPE_CHECKING

from dbnomics_data_model.storage.adapters.filesystem.errors import FileSystemAdapterError

if TYPE_CHECKING:
    from dbnomics_data_model.storage.adapters.filesystem.variants.json_lines.model.json_lines_series_item import (
        JsonLinesSeriesItem,
    )


class JsonLinesSeriesItemError(FileSystemAdapterError):
    pass


class InvalidObservationValue(JsonLinesSeriesItemError):
    def __init__(self, *, json_lines_series_item: "JsonLinesSeriesItem", value_json: float | str) -> None:
        msg = f"The JSON observation value {value_json!r} is invalid"
        super().__init__(msg=msg)
        self.json_lines_series_item = json_lines_series_item
        self.value_json = value_json


class ObservationAttributeCodeTypeError(JsonLinesSeriesItemError):
    def __init__(
        self, *, attribute_codes_json: list[str | None], json_lines_series_item: "JsonLinesSeriesItem"
    ) -> None:
        msg = f"JSON observation attributes are expected to be str, got {type(attribute_codes_json)}"
        super().__init__(msg=msg)
        self.attribute_codes_json = attribute_codes_json
        self.json_lines_series_item = json_lines_series_item


class ObservationPeriodTypeError(JsonLinesSeriesItemError):
    def __init__(self, *, json_lines_series_item: "JsonLinesSeriesItem", period_json: float | str | None) -> None:
        msg = f"The JSON observation period is expected to be a str, got {type(period_json)}"
        super().__init__(msg=msg)
        self.json_lines_series_item = json_lines_series_item
        self.period_json = period_json
