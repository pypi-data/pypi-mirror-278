from collections.abc import Iterator
from pathlib import Path

from stream_unzip import stream_unzip

__all__ = ["extract_file_from_zip_stream"]


def extract_file_from_zip_stream(
    zip_chunks: Iterator[bytes],
    *,
    allow_zip64: bool = True,
    chunk_size: int = 65536,
    file: Path | str,
    password: bytes | None = None,
) -> Iterator[bytes]:
    if isinstance(file, Path):
        file = str(file)

    for file_name, _, unzipped_chunks in stream_unzip(
        zip_chunks, allow_zip64=allow_zip64, chunk_size=chunk_size, password=password
    ):
        # stream_unzip needs unzipped_chunks to be always consumed.
        for chunk in unzipped_chunks:
            if file_name.decode("utf-8") == file:
                yield chunk
