from collections.abc import Iterator
from pathlib import Path

from dbnomics_fetcher_toolbox.file_utils import write_chunks
from dbnomics_fetcher_toolbox.sources.http.requests import RequestsHttpSource

__all__ = ["download_http_url", "fetch_http_url"]


def download_http_url(url: str, *, output_file: Path, response_dump_dir: Path | None = None) -> None:
    response_dump_file = None if response_dump_dir is None else response_dump_dir / f"{output_file.name}.response.txt"
    source_bytes_iter = fetch_http_url(url, response_dump_file=response_dump_file)
    write_chunks(source_bytes_iter, output_file=output_file)


def fetch_http_url(url: str, *, response_dump_file: Path | None = None) -> Iterator[bytes]:
    source = RequestsHttpSource(url)
    return source.iter_bytes(response_dump_file=response_dump_file)
