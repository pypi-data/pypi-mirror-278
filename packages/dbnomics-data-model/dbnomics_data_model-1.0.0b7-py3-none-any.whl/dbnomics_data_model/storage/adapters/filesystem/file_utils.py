import shutil
from collections.abc import Iterator
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dbnomics_data_model.storage.adapters.filesystem.git.tellable_stream import TellableStream


def iter_child_files_or_directories(base_dir: Path, *, ignore_hidden: bool = False) -> Iterator[Path]:
    """Iterate over child files or directories of base_dir."""
    for child in base_dir.iterdir():
        if not child.is_file() and not child.is_dir():
            continue

        child_name = child.name
        if ignore_hidden and child_name.startswith("."):
            continue

        yield child


def iter_child_directories(base_dir: Path, *, ignore_hidden: bool = False) -> Iterator[Path]:
    """Iterate over child directories of base_dir."""
    for child in base_dir.iterdir():
        if not child.is_dir():
            continue

        dir_name = child.name
        if ignore_hidden and dir_name.startswith("."):
            continue

        yield child


def iter_lines_with_offsets(lines: "TellableStream") -> Iterator[tuple[bytes, int]]:
    """Iterate over lines of a file, yielding the line and the offset of the first character of the line."""
    offset = lines.tell()
    for line in lines:
        yield (line, offset)
        offset = lines.tell()


def move_children(source_dir: Path, target_dir: Path, *, ignore_hidden: bool = False, overwrite: bool = False) -> None:
    for child in iter_child_files_or_directories(source_dir, ignore_hidden=ignore_hidden):
        if overwrite:
            target_child = target_dir / child.relative_to(source_dir)
            if target_child.is_dir():
                shutil.rmtree(target_child)
            elif target_child.is_file():
                target_child.unlink()

        shutil.move(child, target_dir)
