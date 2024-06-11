from dataclasses import dataclass
from pathlib import Path

from contexttimer import Timer

from dbnomics_fetcher_toolbox._internal.reports.base_report_builder import BaseReportBuilder
from dbnomics_fetcher_toolbox.types import SectionId

from .types import (
    BaseReportItem,
    BaseSectionStart,
    FailureStatus,
    ReportItemStatus,
    ReportStats,
    SkipStatus,
    SuccessStatus,
)

__all__ = ["DownloadReportBuilder"]


@dataclass(frozen=True, kw_only=True)
class FileReportItem(BaseReportItem):
    file: Path


@dataclass(frozen=True, kw_only=True)
class DownloadReport:
    files: list[FileReportItem]


@dataclass(frozen=True, kw_only=True)
class FileSectionStart(BaseSectionStart):
    file: Path


class DownloadReportBuilder(BaseReportBuilder[FileSectionStart]):
    def __init__(self) -> None:
        super().__init__()
        self._file_report_items: list[FileReportItem] = []

    def get_report(self) -> DownloadReport:
        return DownloadReport(files=self._file_report_items)

    def register_file_section_failure(
        self, section_id: SectionId, *, error: Exception | str, timer: Timer | None = None
    ) -> None:
        file_section_start = self._get_section_start(section_id)
        duration = None if timer is None else timer.elapsed
        self._file_report_items.append(
            FileReportItem(
                file=file_section_start.file,
                section_id=section_id,
                started_at=file_section_start.started_at,
                status=FailureStatus(duration=duration, error=error),
            )
        )

    def register_file_section_skip(self, section_id: SectionId, *, message: str) -> None:
        file_section_start = self._get_section_start(section_id)
        self._file_report_items.append(
            FileReportItem(
                file=file_section_start.file,
                section_id=section_id,
                started_at=file_section_start.started_at,
                status=SkipStatus(message=message),
            )
        )

    def register_file_section_start(self, section_id: SectionId, *, file: Path) -> None:
        self._section_starts.append(FileSectionStart(file=file, section_id=section_id))

    def register_file_section_success(self, section_id: SectionId, *, timer: Timer) -> None:
        file_section_start = self._get_section_start(section_id)
        self._file_report_items.append(
            FileReportItem(
                file=file_section_start.file,
                section_id=section_id,
                started_at=file_section_start.started_at,
                status=SuccessStatus(duration=timer.elapsed),
            )
        )

    @property
    def stats(self) -> "ReportStats":
        def get_count(status: type[ReportItemStatus]) -> int:
            return sum(1 for file_report_item in self._file_report_items if isinstance(file_report_item.status, status))

        return ReportStats(
            failed=get_count(FailureStatus),
            skipped=get_count(SkipStatus),
            succeeded=get_count(SuccessStatus),
        )
