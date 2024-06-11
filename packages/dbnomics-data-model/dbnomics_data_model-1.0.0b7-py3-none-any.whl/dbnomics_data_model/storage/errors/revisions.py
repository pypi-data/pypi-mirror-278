from dbnomics_data_model.errors import DataModelError
from dbnomics_data_model.model.revisions.types import RevisionId


class RevisionsNotAvailable(DataModelError):
    def __init__(self) -> None:
        msg = "Revisions are not available"
        super().__init__(msg=msg)


class LatestRevisionOnlyOperation(DataModelError):
    def __init__(self, *, revision_id: RevisionId) -> None:
        msg = "This operation is only available at the latest revision"
        super().__init__(msg=msg)
        self.revision_id = revision_id
