from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Literal, TypeAlias

from dbnomics_fetcher_toolbox.types import SectionId


@dataclass(frozen=True, kw_only=True)
class FailureStatus:
    duration: float | None
    error: Exception | str
    type: Literal["failure"] = field(default="failure")


@dataclass(frozen=True, kw_only=True)
class SkipStatus:
    message: str
    type: Literal["skip"] = field(default="skip")


@dataclass(frozen=True, kw_only=True)
class SuccessStatus:
    duration: float
    type: Literal["success"] = field(default="success")


ReportItemStatus: TypeAlias = FailureStatus | SkipStatus | SuccessStatus


@dataclass(frozen=True, kw_only=True)
class BaseSectionStart:
    section_id: SectionId
    started_at: datetime = field(default_factory=lambda: datetime.now(tz=timezone.utc))


@dataclass(frozen=True, kw_only=True)
class BaseReportItem:
    section_id: SectionId
    started_at: datetime
    status: ReportItemStatus


@dataclass(frozen=True, kw_only=True)
class ReportStats:
    failed: int
    skipped: int
    succeeded: int

    @property
    def total(self) -> int:
        return self.failed + self.skipped + self.succeeded
