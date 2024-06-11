from collections.abc import Iterable, Iterator
from itertools import chain

from more_itertools import windowed

from dbnomics_data_model.model.revisions.constants import NULL_REVISION, NullRevision
from dbnomics_data_model.model.revisions.revision import Revision


def iter_revision_pairs(revisions: Iterable[Revision]) -> Iterator[tuple[Revision, Revision | NullRevision]]:
    for revision, previous_revision in windowed(chain(revisions, [NULL_REVISION]), 2):
        assert isinstance(revision, Revision)
        assert isinstance(previous_revision, NullRevision | Revision)
        yield revision, previous_revision
