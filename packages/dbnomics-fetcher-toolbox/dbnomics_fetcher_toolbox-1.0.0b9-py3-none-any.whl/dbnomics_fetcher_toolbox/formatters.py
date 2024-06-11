from pathlib import Path

from humanfriendly import format_size

__all__ = ["format_file_path_with_size"]


def format_file_path_with_size(file_path: Path) -> str:
    path_str = f"{str(file_path)!r}"
    size_str = format_size(file_path.stat().st_size, binary=True) if file_path.exists() else "does not exist"
    return f"{path_str} ({size_str})"
