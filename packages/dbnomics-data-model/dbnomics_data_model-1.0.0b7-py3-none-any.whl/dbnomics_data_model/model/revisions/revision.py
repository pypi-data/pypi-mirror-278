from dataclasses import dataclass, field
from datetime import datetime

from dbnomics_data_model.model.revisions.types import RevisionId, RevisionMetadata


@dataclass(frozen=True, kw_only=True)
class Revision:
    author_email: str | None
    author_name: str
    created_at: datetime
    id: RevisionId
    message: str = field(repr=False)

    metadata: RevisionMetadata = field(default_factory=dict)

    def __str__(self) -> str:
        return self.id
