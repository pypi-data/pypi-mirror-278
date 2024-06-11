from dataclasses import dataclass

from contexttimer import Timer
from dbnomics_data_model.model import DatasetCode
from typedload.datadumper import Dumper

from dbnomics_fetcher_toolbox._internal.reports.base_report_builder import BaseReportBuilder
from dbnomics_fetcher_toolbox._internal.typedload_utils import add_handler
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

__all__ = ["ConvertReportBuilder"]


@dataclass(frozen=True, kw_only=True)
class DatasetReportItem(BaseReportItem):
    dataset_code: DatasetCode


@dataclass(frozen=True, kw_only=True)
class ConvertReport:
    datasets: list[DatasetReportItem]


@dataclass(frozen=True, kw_only=True)
class DatasetSectionStart(BaseSectionStart):
    dataset_code: DatasetCode


class ConvertReportBuilder(BaseReportBuilder[DatasetSectionStart]):
    def __init__(self) -> None:
        super().__init__()
        self._dataset_report_items: list[DatasetReportItem] = []

    def get_report(self) -> ConvertReport:
        return ConvertReport(datasets=self._dataset_report_items)

    def register_dataset_section_failure(
        self, section_id: SectionId, *, error: Exception | str, timer: Timer | None = None
    ) -> None:
        dataset_section_start = self._get_section_start(section_id)
        duration = None if timer is None else timer.elapsed
        self._dataset_report_items.append(
            DatasetReportItem(
                dataset_code=dataset_section_start.dataset_code,
                section_id=section_id,
                started_at=dataset_section_start.started_at,
                status=FailureStatus(duration=duration, error=error),
            )
        )

    def register_file_section_skip(self, section_id: SectionId, *, message: str) -> None:
        dataset_section_start = self._get_section_start(section_id)
        self._dataset_report_items.append(
            DatasetReportItem(
                dataset_code=dataset_section_start.dataset_code,
                section_id=section_id,
                started_at=dataset_section_start.started_at,
                status=SkipStatus(message=message),
            )
        )

    def register_dataset_section_start(self, section_id: SectionId, *, dataset_code: DatasetCode) -> None:
        self._section_starts.append(DatasetSectionStart(section_id=section_id, dataset_code=dataset_code))

    def register_dataset_section_success(self, section_id: SectionId, *, timer: Timer) -> None:
        dataset_section_start = self._get_section_start(section_id)
        self._dataset_report_items.append(
            DatasetReportItem(
                dataset_code=dataset_section_start.dataset_code,
                section_id=section_id,
                started_at=dataset_section_start.started_at,
                status=SuccessStatus(duration=timer.elapsed),
            )
        )

    @property
    def stats(self) -> "ReportStats":
        def get_count(status: type[ReportItemStatus]) -> int:
            return sum(
                1
                for dataset_report_item in self._dataset_report_items
                if isinstance(dataset_report_item.status, status)
            )

        return ReportStats(
            failed=get_count(FailureStatus),
            skipped=get_count(SkipStatus),
            succeeded=get_count(SuccessStatus),
        )

    def _create_dumper(self) -> Dumper:
        dumper = super()._create_dumper()
        add_handler(
            dumper,
            (
                lambda x: isinstance(x, DatasetCode),
                lambda _dumper, value, _value_type: str(value),
            ),
            sample_value=DatasetCode.parse("D1"),
        )
        return dumper
