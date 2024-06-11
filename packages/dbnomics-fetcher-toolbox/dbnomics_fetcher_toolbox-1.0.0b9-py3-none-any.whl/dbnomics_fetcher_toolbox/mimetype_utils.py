import mimetypes
from pathlib import Path

import magic
from pantomime import normalize_mimetype

from dbnomics_fetcher_toolbox.errors.mimetype_utils import InvalidMimeType, MimeTypeNotGuessed

__all__ = ["validate_mimetype"]


def validate_mimetype(input_file: Path, *, expected_mimetype: str | None = None) -> None:
    if expected_mimetype is None:
        expected_mimetype, _ = mimetypes.guess_type(input_file)
    if expected_mimetype is None:
        raise MimeTypeNotGuessed(input_file=input_file)
    expected_mimetype = normalize_mimetype(expected_mimetype)

    detected_mimetype = magic.from_file(input_file, mime=True)
    detected_mimetype = normalize_mimetype(detected_mimetype)

    if detected_mimetype != expected_mimetype:
        raise InvalidMimeType(detected_mimetype=detected_mimetype, expected_mimetype=expected_mimetype)
