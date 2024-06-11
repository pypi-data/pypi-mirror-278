from pathlib import Path

from dbnomics_fetcher_toolbox.errors.base import FetcherToolboxError
from dbnomics_fetcher_toolbox.formatters import format_file_path_with_size


class InvalidMimeType(FetcherToolboxError):
    def __init__(self, *, detected_mimetype: str, expected_mimetype: str) -> None:
        msg = f"The detected MIME type ({detected_mimetype}) differs from the expected one ({expected_mimetype})"
        super().__init__(msg=msg)
        self.detected_mimetype = detected_mimetype
        self.expected_mimetype = expected_mimetype


class MimeTypeNotGuessed(FetcherToolboxError):
    def __init__(self, *, input_file: Path) -> None:
        msg = f"The MIME type of {format_file_path_with_size(input_file)} could not be guessed from the file name"
        super().__init__(msg=msg)
        self.input_file = input_file
