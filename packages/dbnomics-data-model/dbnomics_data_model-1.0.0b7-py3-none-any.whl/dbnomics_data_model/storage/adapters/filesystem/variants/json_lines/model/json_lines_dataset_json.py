from dbnomics_data_model.storage.adapters.filesystem.model.base_dataset_json import BaseDatasetJson

__all__ = ["JsonLinesDatasetJson"]


class JsonLinesDatasetJson(BaseDatasetJson):
    """Model for dataset.json following the JSON lines storage variant.

    Contains dataset metadata.

    Series metadata is stored in series.jsonl.
    """
