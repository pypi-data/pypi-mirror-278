from abc import abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING

import daiquiri

from dbnomics_fetcher_toolbox._internal.formatters import format_csv_values
from dbnomics_fetcher_toolbox._internal.reports.convert_report_builder import ConvertReportBuilder
from dbnomics_fetcher_toolbox._internal.reports.download_report_builder import DownloadReportBuilder
from dbnomics_fetcher_toolbox.formatters import format_file_path_with_size
from dbnomics_fetcher_toolbox.types import SectionId

if TYPE_CHECKING:
    from dbnomics_fetcher_toolbox.types import SectionId

__all__ = ["BaseFetcherHelper"]


logger = daiquiri.getLogger(__name__)


class BaseFetcherHelper:
    def __init__(
        self,
        *,
        excluded: list["SectionId"] | None = None,
        fail_fast: bool = False,
        report_file: Path | None = None,
        resume_mode: bool = True,
        selected: list["SectionId"] | None = None,
    ) -> None:
        self._excluded = excluded
        self._fail_fast = fail_fast

        self._report_file = report_file
        self._resume_mode = resume_mode
        self._selected = selected

        self._matched_excluded: set[SectionId] = set()
        self._matched_selected: set[SectionId] = set()

        if self._excluded:
            logger.debug("Will skip those excluded sections: %s", format_csv_values(self._excluded))
        if self._selected:
            logger.debug("Will process only those selected sections: %s", format_csv_values(self._selected))

    @abstractmethod
    def _get_report_builder(self) -> DownloadReportBuilder | ConvertReportBuilder: ...

    def _is_section_skipped_for_options(self, section_id: "SectionId") -> str | None:
        if self._excluded is not None and section_id in self._excluded:
            self._matched_excluded.add(section_id)
            return f"Skipping section {section_id!r} because it was excluded"

        if self._selected is not None:
            if section_id in self._selected:
                self._matched_selected.add(section_id)
            else:
                return f"Skipping section {section_id!r} because it was not selected"

        return None

    def _log_stats(self) -> None:
        logger.info(self._get_report_builder().stats)

    def _log_unmatched_filters(self) -> None:
        if self._excluded is not None and (unmatched_excluded := set(self._excluded) - self._matched_excluded):
            logger.warning(
                "The following excluded sections were never processed: %s",
                format_csv_values(unmatched_excluded),
            )

        if self._selected is not None and (unmatched_selected := set(self._selected) - self._matched_selected):
            logger.warning(
                "The following selected sections were never processed: %s",
                format_csv_values(unmatched_selected),
            )

    def _save_report(self) -> None:
        if self._report_file is None:
            logger.debug("Skip saving the report because no file path has been given")
            return

        report_builder = self._get_report_builder()
        report_builder.save_report(self._report_file)
        logger.info("The report has been saved to %s", format_file_path_with_size(self._report_file))
