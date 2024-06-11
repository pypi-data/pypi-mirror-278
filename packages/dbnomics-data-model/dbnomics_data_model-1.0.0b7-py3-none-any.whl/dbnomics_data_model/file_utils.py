from pathlib import Path

from humanfriendly import format_size


def format_file_path_with_size(file_path: Path) -> str:
    path_str = f"{str(file_path)!r}"
    size_str = format_size(file_path.stat().st_size, binary=True) if file_path.exists() else "does not exist"
    return f"{path_str} ({size_str})"


def write_gitignore_all(directory: Path, *, exist_ok: bool = False) -> None:
    """Write a .gitignore file ignoring the whole directory to avoid committing it accidentally."""
    gitignore_filename = ".gitignore"
    gitignore_file = directory / gitignore_filename

    if gitignore_file.is_file():
        if exist_ok:
            return
        msg = f"{gitignore_filename} already exists in {directory}"
        raise RuntimeError(msg)

    gitignore_file.write_text("*")
