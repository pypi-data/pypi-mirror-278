from collections.abc import Callable, Container
from datetime import timedelta
from typing import TYPE_CHECKING, Final

import daiquiri
import requests.exceptions
from humanfriendly import format_timespan
from tenacity import Retrying, retry_if_exception, retry_if_exception_type, stop_after_attempt, wait_exponential

if TYPE_CHECKING:
    from tenacity import RetryCallState


__all__ = [
    "default_retrying_retry",
    "default_retrying_stop",
    "default_retrying_wait",
    "default_retrying",
    "retry_if_bad_http_status_code",
]


logger = daiquiri.getLogger(__name__)


def log_before_attempt(retry_state: "RetryCallState") -> None:
    logger.debug("Loading source, attempt %d", retry_state.attempt_number)


def log_before_sleep(retry_state: "RetryCallState") -> None:
    assert retry_state.next_action is not None
    sleep_duration = retry_state.next_action.sleep
    logger.debug("Sleeping %s", format_timespan(sleep_duration))


def log_failed_attempt(retry_state: "RetryCallState") -> None:
    outcome = retry_state.outcome
    assert outcome is not None

    msg = "Error loading source"

    duration = retry_state.seconds_since_start
    if duration is not None:
        msg += f" after {format_timespan(duration)}"

    msg += f", attempt {retry_state.attempt_number}"

    try:
        outcome.result()
    except Exception:
        logger.exception(msg)
    else:
        logger.error(msg)


default_http_codes_to_retry: Final = {
    408,  # Request Timeout
    425,  # Too Early
    429,  # Too Many Requests
    500,  # Internal Server Error
    502,  # Bad Gateway
    503,  # Service Unavailable
    504,  # Gateway Timeout
}


def make_should_retry_http_status_code(
    http_codes_to_retry: Container[int] | None = None,
) -> Callable[[BaseException], bool]:
    if http_codes_to_retry is None:
        http_codes_to_retry = default_http_codes_to_retry

    def should_retry_http_status_code(exception: BaseException) -> bool:
        if isinstance(exception, requests.exceptions.HTTPError):
            status_code = exception.response.status_code  # type: ignore[union-attr]
            return status_code in http_codes_to_retry

        return False

    return should_retry_http_status_code


should_retry_http_status_code: Final = make_should_retry_http_status_code()
retry_if_bad_http_status_code: Final = retry_if_exception(predicate=should_retry_http_status_code)
default_http_exceptions_to_retry: Final = {
    requests.exceptions.ChunkedEncodingError,
    requests.exceptions.ConnectionError,
    requests.exceptions.Timeout,
}


retry_if_http_exception: Final = retry_if_exception_type(tuple(default_http_exceptions_to_retry))
default_retrying_retry: Final = retry_if_bad_http_status_code | retry_if_http_exception
default_retrying_stop: Final = stop_after_attempt(5)
default_retrying_wait: Final = wait_exponential(max=timedelta(minutes=5), multiplier=1.5)
default_retrying: Final = Retrying(
    after=log_failed_attempt,
    before=log_before_attempt,
    before_sleep=log_before_sleep,
    retry=default_retrying_retry,
    stop=default_retrying_stop,
    wait=default_retrying_wait,
)
