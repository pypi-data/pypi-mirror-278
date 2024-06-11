from collections.abc import Iterator
from pathlib import Path

import daiquiri
from humanfriendly import format_size

__all__ = ["iter_child_directories", "write_chunks"]

logger = daiquiri.getLogger(__name__)


def iter_child_directories(base_dir: Path, *, ignore_hidden: bool = True) -> Iterator[Path]:
    """Iterate over child directories of base_dir."""
    for child in base_dir.iterdir():
        if not child.is_dir():
            continue

        dir_name = child.name
        if ignore_hidden and dir_name.startswith("."):
            continue

        yield child


def write_chunks(
    chunks: Iterator[bytes],
    *,
    output_file: Path,
    page_size: int = 1024,
    message_interval: int = 1024,
) -> None:
    total_bytes_written = 0
    page_num = 1

    partial_output_file = output_file.with_suffix(f"{output_file.suffix}.part")
    output_file.parent.mkdir(exist_ok=True, parents=True)  # in case output_file == "source-data/datasets/dataset1.xml"

    with partial_output_file.open("wb") as fp:
        while True:
            try:
                chunk = next(chunks)
            except StopIteration:
                break

            fp.write(chunk)
            total_bytes_written += len(chunk)

            if total_bytes_written >= page_size * page_num * message_interval:
                logger.debug("%s bytes have been written so far", format_size(total_bytes_written, binary=True))
                page_num += 1

    partial_output_file.replace(output_file)
