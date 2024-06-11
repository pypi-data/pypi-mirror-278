from collections.abc import Callable, Iterator
from pathlib import Path
from typing import TYPE_CHECKING, Final, Self, TypeAlias

import daiquiri
from git import GitError, Repo
from git.objects import Blob, Commit, Tree
from jsonalias import Json

from dbnomics_data_model.json_utils.errors import JsonParseError
from dbnomics_data_model.json_utils.parsing import parse_json_bytes
from dbnomics_data_model.model.identifiers.dataset_code import DatasetCode
from dbnomics_data_model.model.identifiers.errors import DatasetCodeParseError
from dbnomics_data_model.model.revisions.types import RevisionId
from dbnomics_data_model.storage.adapters.filesystem.constants import DATASET_JSON
from dbnomics_data_model.storage.adapters.filesystem.errors.git_provider_directory_manager import (
    BlobExpected,
    BlobNotFound,
    BlobParseError,
    CommitExpected,
    RepositoryDirectoryNotFound,
    RepositoryOpenError,
    RevisionNotFound,
    TreeExpected,
    TreeNotFound,
)
from dbnomics_data_model.storage.adapters.filesystem.git.git_revision import GitRevision
from dbnomics_data_model.storage.adapters.filesystem.git.git_utils import read_blob

if TYPE_CHECKING:
    from git.objects.base import IndexObjUnion

__all__ = ["GitProviderDirectoryManager"]


logger = daiquiri.getLogger(__name__)

TreeIndex: TypeAlias = str | Path | int

DEFAULT_REVISION: Final = "HEAD"

NULL_PATH: Final = "."


class GitProviderDirectoryManager:
    def __init__(self, *, repo: Repo) -> None:
        self._repo = repo

    @classmethod
    def open(cls, repo_dir: Path | str) -> Self:
        if isinstance(repo_dir, str):
            repo_dir = Path(repo_dir)

        if not repo_dir.is_dir():
            raise RepositoryDirectoryNotFound(repo_dir=repo_dir)

        try:
            repo = Repo(repo_dir)
        except GitError as exc:
            raise RepositoryOpenError(repo_dir=repo_dir) from exc

        return cls(repo=repo)

    def has_dir(self, directory: Path | str, *, revision_id: RevisionId | None = None) -> bool:
        if revision_id is None:
            revision_id = DEFAULT_REVISION

        commit = self._get_commit(revision_id)
        dir_relative_path = self._get_relative_path(directory)

        try:
            self._get_tree(commit.tree, str(dir_relative_path))
        except TreeNotFound:
            return False

        return True

    def has_file(self, file: Path | str, *, revision_id: RevisionId | None = None) -> bool:
        if revision_id is None:
            revision_id = DEFAULT_REVISION

        commit = self._get_commit(revision_id)
        file_relative_path = self._get_relative_path(file)

        try:
            self._get_blob(commit.tree, file_relative_path)
        except BlobNotFound:
            return False

        return True

    def iter_blobs_matching_name(
        self,
        blob_name_matcher: Callable[[Path], bool],
        *,
        revision_id: RevisionId | None = None,
        sub_tree: Path | str | None = None,
    ) -> Iterator[Blob]:
        if revision_id is None:
            revision_id = DEFAULT_REVISION

        commit = self._get_commit(revision_id)

        if sub_tree is not None:
            tree = self._get_tree(commit.tree, sub_tree)

        for blob in self._iter_blobs(tree):
            if blob_name_matcher(Path(blob.name)):
                yield blob

    def iter_dataset_directories(self, *, revision_id: RevisionId | None = None) -> Iterator[tuple[DatasetCode, Path]]:
        if revision_id is None:
            revision_id = DEFAULT_REVISION

        commit = self._get_commit(revision_id)

        logger.debug(
            "Iterating over dataset directories from Git repository %s at revision %s", str(self.repo_dir), revision_id
        )

        for tree in self._iter_trees(commit.tree):
            dir_name = tree.name

            if dir_name is None:
                logger.debug("Ignoring sub-tree without name: %r", tree)
                continue

            if dir_name.startswith("."):
                logger.debug("Ignoring hidden directory: %r", dir_name)
                continue

            try:
                self._get_blob(tree, DATASET_JSON)
            except BlobNotFound:
                logger.debug("Ignoring directory without a %r file", DATASET_JSON, tree=tree)
                continue

            try:
                dataset_code = DatasetCode.parse(dir_name)
            except DatasetCodeParseError:
                logger.exception("Ignoring directory %r which name is not a dataset code", dir_name)
                continue

            dataset_dir = self.repo_dir / dir_name
            logger.debug("Found dataset directory: %r", dir_name)
            yield dataset_code, dataset_dir

    def iter_repo_revisions(self, start_revision_id: RevisionId | None = None) -> Iterator[GitRevision]:
        for commit in self._iter_commits(start_revision_id):
            yield GitRevision.from_commit(commit)

    def load_blob(self, file: Path | str, *, revision_id: RevisionId | None = None) -> Blob:
        if revision_id is None:
            revision_id = DEFAULT_REVISION

        commit = self._get_commit(revision_id)
        file_relative_path = self._get_relative_path(file)
        return self._get_blob(commit.tree, file_relative_path)

    def load_blob_as_bytes(self, file: Path | str, *, revision_id: RevisionId | None = None) -> bytes:
        if revision_id is None:
            revision_id = DEFAULT_REVISION

        file_relative_path = self._get_relative_path(file)

        blob = self.load_blob(file_relative_path, revision_id=revision_id)
        return read_blob(blob)

    def load_json_file(self, file: Path | str, *, revision_id: RevisionId | None = None) -> Json:
        if revision_id is None:
            revision_id = DEFAULT_REVISION

        file_relative_path = self._get_relative_path(file)
        blob_bytes = self.load_blob_as_bytes(file_relative_path, revision_id=revision_id)

        try:
            data = parse_json_bytes(blob_bytes)
        except JsonParseError as exc:
            raise BlobParseError(
                blob_bytes=blob_bytes, file_relative_path=file_relative_path, repo=self._repo, revision_id=revision_id
            ) from exc

        return data

    @property
    def repo_dir(self) -> Path:
        return Path(self._repo.working_dir)

    def _get_blob(self, tree: Tree, index: TreeIndex) -> Blob:
        try:
            obj = self._get_object(tree, index)
        except KeyError as exc:
            raise BlobNotFound(index=index, repo=self._repo, tree=tree) from exc

        if not isinstance(obj, Blob):
            raise BlobExpected(index=index, object_type=str(obj.type), repo=self._repo, tree=tree)

        return obj

    def _get_commit(self, revision_id: RevisionId) -> Commit:
        try:
            obj = self._repo.rev_parse(revision_id)
        except KeyError as exc:
            raise RevisionNotFound(repo=self._repo, revision_id=revision_id) from exc

        if not isinstance(obj, Commit):
            raise CommitExpected(object_type=str(obj.type), repo=self._repo, revision_id=revision_id)

        return obj

    def _get_object(self, tree: Tree, index: TreeIndex) -> "IndexObjUnion":
        return tree[str(index)]

    def _get_relative_path(self, path: Path | str) -> Path:
        if isinstance(path, str):
            path = Path(path)

        if path.is_absolute():
            return path.relative_to(self.repo_dir)

        return path

    def _get_tree(self, tree: Tree, index: TreeIndex) -> Tree:
        if isinstance(index, Path | str) and str(index) == NULL_PATH:
            return tree

        try:
            obj = self._get_object(tree, index)
        except KeyError as exc:
            raise TreeNotFound(index=index, repo=self._repo, tree=tree) from exc

        if not isinstance(obj, Tree):
            raise TreeExpected(index=index, object_type=obj.type, repo=self._repo, tree=tree)

        return obj

    def _iter_blobs(self, tree: Tree) -> Iterator[Blob]:
        for obj in tree:
            if isinstance(obj, Blob):
                yield obj

    def _iter_commits(self, start_revision_id: RevisionId | None = None) -> Iterator[Commit]:
        if start_revision_id is None:
            start_revision_id = DEFAULT_REVISION

        logger.debug(
            "Iterating over commits of Git repository %s starting from commit %s", str(self.repo_dir), start_revision_id
        )

        commit = self._get_commit(start_revision_id)

        yield from self._repo.iter_commits(commit)

    def _iter_trees(self, tree: Tree) -> Iterator[Tree]:
        for obj in tree:
            if isinstance(obj, Tree):
                yield obj
