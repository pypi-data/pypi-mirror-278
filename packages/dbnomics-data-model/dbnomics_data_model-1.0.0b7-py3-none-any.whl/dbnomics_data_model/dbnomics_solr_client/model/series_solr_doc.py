from dataclasses import dataclass

from dbnomics_data_model.storage.adapters.filesystem.variants.json_lines.offsets.types import JsonLinesOffset


@dataclass(frozen=True, kw_only=True)
class SeriesSolrDoc:
    id: str
    series_jsonl_offset: JsonLinesOffset | None = None
