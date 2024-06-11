from pathlib import Path
from typing import TYPE_CHECKING

from dbnomics_data_model.model.revisions.types import RevisionId
from dbnomics_data_model.storage.adapters.filesystem.errors import FileSystemAdapterError

if TYPE_CHECKING:
    from git import Repo
    from git.objects import Tree

    from dbnomics_data_model.storage.adapters.filesystem.git.git_provider_directory_manager import TreeIndex


class GitProviderDirectoryManagerError(FileSystemAdapterError):
    pass


class BlobExpected(GitProviderDirectoryManagerError):
    def __init__(self, *, index: "TreeIndex", object_type: str, repo: "Repo", tree: "Tree") -> None:
        msg = f"Expected a blob but found {object_type!r} at index {str(index)!r} of the tree {tree.hexsha!r} in the Git repository at {repo.working_dir}"  # noqa: E501
        super().__init__(msg=msg)
        self.index = index
        self.object_type = object_type
        self.repo = repo
        self.tree = tree


class BlobNotFound(GitProviderDirectoryManagerError):
    def __init__(self, *, index: "TreeIndex", repo: "Repo", tree: "Tree") -> None:
        msg = f"Blob not found at index {str(index)!r} of the tree {tree.hexsha!r} in the Git repository at {repo.working_dir}"  # noqa: E501
        super().__init__(msg=msg)
        self.index = index
        self.repo = repo
        self.tree = tree


class BlobParseError(GitProviderDirectoryManagerError):
    def __init__(self, *, blob_bytes: bytes, file_relative_path: Path, repo: "Repo", revision_id: RevisionId) -> None:
        msg = f"Could not parse blob data of file {str(file_relative_path)!r} at revision {revision_id} as JSON from the Git repository at {repo.working_dir}"  # noqa: E501
        super().__init__(msg=msg)
        self.blob_bytes = blob_bytes
        self.file_relative_path = file_relative_path
        self.repo = repo
        self.revision_id = revision_id


class CommitExpected(GitProviderDirectoryManagerError):
    def __init__(self, *, object_type: str, repo: "Repo", revision_id: RevisionId) -> None:
        msg = f"Expected a commit but found {object_type!r} at revision {revision_id!r} in the Git repository at {repo.working_dir}"  # noqa: E501
        super().__init__(msg=msg)
        self.object_type = object_type
        self.repo = repo
        self.revision_id = revision_id


class RepositoryDirectoryNotFound(GitProviderDirectoryManagerError):
    def __init__(self, *, repo_dir: Path) -> None:
        msg = f"Could not find the directory {repo_dir} to open a Git repository from"
        super().__init__(msg=msg)
        self.repo_dir = repo_dir


class RepositoryOpenError(GitProviderDirectoryManagerError):
    def __init__(self, *, repo_dir: Path) -> None:
        msg = f"Could not open a Git repository from {repo_dir}"
        super().__init__(msg=msg)
        self.repo_dir = repo_dir


class RevisionNotFound(GitProviderDirectoryManagerError):
    def __init__(self, *, revision_id: RevisionId, repo: "Repo") -> None:
        msg = f"Could not find revision {revision_id!r} in the Git repository at {repo.working_dir}"
        super().__init__(msg=msg)
        self.repo = repo
        self.revision_id = revision_id


class TreeExpected(GitProviderDirectoryManagerError):
    def __init__(self, *, index: "TreeIndex", object_type: str, repo: "Repo", tree: "Tree") -> None:
        msg = f"Expected a tree but found {object_type!r} at index {str(index)!r} of the tree {tree.hexsha!r} in the Git repository at {repo.working_dir}"  # noqa: E501
        super().__init__(msg=msg)
        self.index = index
        self.object_type = object_type
        self.repo = repo
        self.tree = tree


class TreeNotFound(GitProviderDirectoryManagerError):
    def __init__(self, *, index: "TreeIndex", repo: "Repo", tree: "Tree") -> None:
        msg = f"Tree not found at index {str(index)!r} of the tree {tree.hexsha!r} in the Git repository at {repo.working_dir}"  # noqa: E501
        super().__init__(msg=msg)
        self.index = index
        self.repo = repo
        self.tree = tree
