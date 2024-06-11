from collections.abc import Callable
from typing import Any, TypeAlias

from typedload.datadumper import Dumper
from typedload.exceptions import TypedloadValueError

TypedloadHandler: TypeAlias = tuple[Callable[[Any], bool], Callable[[Dumper, Any, type], Any]]


def add_handler(dumper: Dumper, handler: TypedloadHandler, *, sample_value: Any) -> None:
    try:
        index = dumper.index(sample_value)
    except TypedloadValueError:
        index = len(dumper.handlers)
    dumper.handlers.insert(index, handler)
