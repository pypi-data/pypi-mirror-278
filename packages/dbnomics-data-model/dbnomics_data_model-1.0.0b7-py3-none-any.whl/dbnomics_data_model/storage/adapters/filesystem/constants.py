from typing import Final

from dbnomics_data_model.model.identifiers import ProviderCode

NOT_AVAILABLE: Final = "NA"

CATEGORY_TREE_JSON: Final = "category_tree.json"
DATASET_JSON: Final = "dataset.json"
PROVIDER_JSON: Final = "provider.json"
RELEASES_JSON: Final = "releases.json"
SERIES_JSONL: Final = "series.jsonl"

UNKNOWN_PROVIDER_CODE: Final = ProviderCode("__UNKNOWN__")

BASE_SESSION_DIR_NAME: Final = ".sessions"
