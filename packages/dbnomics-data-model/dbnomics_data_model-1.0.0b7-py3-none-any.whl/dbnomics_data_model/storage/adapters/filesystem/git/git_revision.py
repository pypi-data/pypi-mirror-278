from dataclasses import dataclass, field
from typing import Self

from git.objects import Commit

from dbnomics_data_model.model.revisions.revision import Revision


@dataclass(frozen=True, kw_only=True)
class GitRevision(Revision):
    commit: Commit = field(repr=False)

    def __post_init__(self) -> None:
        commit_hex = self.commit.hexsha
        if commit_hex != self.id:
            msg = f"Git commit hex {commit_hex} is different from {self.id=}"
            raise ValueError(msg)

    @classmethod
    def from_commit(cls, commit: Commit) -> Self:
        author_name = commit.author.name
        if author_name is None:
            msg = f"Author of commit {commit.hexsha!r} has no name"
            raise RuntimeError(msg)

        return cls(
            author_email=commit.author.email,
            author_name=author_name,
            commit=commit,
            created_at=commit.committed_datetime,
            id=commit.hexsha,
            message=str(commit.message),
        )
