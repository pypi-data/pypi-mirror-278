from argparse import ArgumentTypeError
from collections.abc import Callable, Iterator
from typing import TypeVar

from dbnomics_data_model.model import DatasetCode
from dbnomics_data_model.model.identifiers.errors import DatasetCodeParseError
from dbnomics_data_model.storage import StorageUri, parse_storage_uri
from dbnomics_data_model.storage.errors.storage_uri import StorageUriParseError

from dbnomics_fetcher_toolbox.types import SectionId

TNumber = TypeVar("TNumber", int, float)


def csv_section_ids(value: str) -> list[SectionId]:
    items = csv_str(value)
    return [SectionId.parse(item) for item in items]


def csv_str(value: str) -> list[str]:
    """Transform a string containing comma-separated values to a list of strings.

    If the input string has spaces around commas, they are removed.

    >>> csv_str('')
    []
    >>> csv_str('a')
    ['a']
    >>> csv_str('a,b')
    ['a', 'b']
    """

    def iter_parts(parts: list[str]) -> Iterator[str]:
        for part in parts:
            part = part.strip()  # noqa: PLW2901
            if not part:
                msg = f"Invalid input: {value}"
                raise ArgumentTypeError(msg)
            yield part

    if not value:
        return []
    return list(iter_parts(value.split(",")))


def dataset_code(value: str) -> DatasetCode:
    try:
        return DatasetCode.parse(value)
    except DatasetCodeParseError as exc:
        msg = f"{value!r} is not a valid dataset code"
        raise ArgumentTypeError(msg) from exc


def positive(numeric_type: type[TNumber]) -> Callable[[str], TNumber]:
    def require_positive(value: str) -> TNumber:
        number = numeric_type(value)
        if number <= 0:
            msg = f"{value!r} is not a positive number"
            raise ArgumentTypeError(msg)
        return number

    return require_positive


def storage_uri(value: str) -> StorageUri:
    try:
        return parse_storage_uri(value)
    except StorageUriParseError as exc:
        raise ArgumentTypeError(str(exc)) from exc
