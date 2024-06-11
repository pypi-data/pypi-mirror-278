from abc import abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING, Generic, TypeVar

from dbnomics_data_model.json_utils import dump_as_json_bytes
from typedload.datadumper import Dumper

from dbnomics_fetcher_toolbox._internal.reports.error_chain import build_error_chain
from dbnomics_fetcher_toolbox._internal.typedload_utils import add_handler
from dbnomics_fetcher_toolbox.types import SectionId

if TYPE_CHECKING:
    from dbnomics_fetcher_toolbox._internal.reports.convert_report_builder import ConvertReport
    from dbnomics_fetcher_toolbox._internal.reports.download_report_builder import DownloadReport
    from dbnomics_fetcher_toolbox._internal.reports.types import BaseSectionStart


T = TypeVar("T", bound="BaseSectionStart")


class BaseReportBuilder(Generic[T]):
    def __init__(self) -> None:
        self._dumper = self._create_dumper()
        self._section_starts: list[T] = []

    @abstractmethod
    def get_report(self) -> "ConvertReport | DownloadReport": ...

    def save_report(self, output_file: Path) -> None:
        report = self.get_report()
        report_bytes = dump_as_json_bytes(report, dumper=self._dumper)
        output_file.write_bytes(report_bytes)

    def _create_dumper(self) -> Dumper:
        dumper = Dumper(hidedefault=False, isodates=True)
        dumper.strconstructed.add(SectionId)  # type: ignore[reportUnknownMemberType]
        add_handler(
            dumper,
            (
                lambda x: isinstance(x, BaseException),
                lambda _dumper, value, _value_type: build_error_chain(value),
            ),
            sample_value=Exception("sample"),
        )
        return dumper

    def _find_section_start(self, section_id: SectionId) -> T | None:
        for section_start in self._section_starts:
            if section_start.section_id == section_id:
                return section_start

        return None

    def _get_section_start(self, section_id: SectionId) -> T:
        section_start = self._find_section_start(section_id)
        if section_start is None:
            msg = f"Section start item was not found for {section_id=}"
            raise AssertionError(msg)

        return section_start
