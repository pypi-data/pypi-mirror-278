from collections.abc import Iterable
from typing import Any

from contexttimer import Timer
from humanfriendly import format_timespan


def format_csv_values(values: Iterable[Any]) -> str:
    return ", ".join(sorted(map(str, values)))


def format_timer(timer: Timer) -> str:
    return format_timespan(timer.elapsed)
