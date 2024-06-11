from typing import TypeAlias

from dbnomics_data_model.types import SupportsStr

RevisionId: TypeAlias = str

RevisionMetadata: TypeAlias = dict[str, SupportsStr]
