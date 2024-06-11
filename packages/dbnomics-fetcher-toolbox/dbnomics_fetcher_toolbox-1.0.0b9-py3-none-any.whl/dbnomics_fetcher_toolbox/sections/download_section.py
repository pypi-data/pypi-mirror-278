from collections.abc import Iterator
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Self

import daiquiri
from contexttimer import Timer

from dbnomics_fetcher_toolbox._internal.formatters import format_csv_values, format_timer
from dbnomics_fetcher_toolbox._internal.reports.download_report_builder import DownloadReportBuilder
from dbnomics_fetcher_toolbox.formatters import format_file_path_with_size
from dbnomics_fetcher_toolbox.sections.base_section import BaseSection
from dbnomics_fetcher_toolbox.types import SectionId

if TYPE_CHECKING:
    from dbnomics_fetcher_toolbox.helpers.downloader_helper import DownloaderHelper
    from dbnomics_fetcher_toolbox.sections.file_section import FileSection


__all__ = ["DownloadSection"]


logger = daiquiri.getLogger(__name__)


class DownloadSection(BaseSection):
    def __init__(
        self,
        *,
        downloader_helper: "DownloaderHelper",
        fail_fast: bool,
        id: SectionId | str,
        parent_path: list[SectionId],
        report_builder: DownloadReportBuilder,
        resume_mode: bool,
    ) -> None:
        super().__init__(fail_fast=fail_fast, id=id, parent_path=parent_path, resume_mode=resume_mode)

        self._downloader_helper = downloader_helper
        self._report_builder = report_builder

        self._file_subsections: list[FileSection] = []

    @property
    def is_skipped(self) -> bool:
        if reason := self._downloader_helper._is_section_skipped_for_options(self.id):  # noqa: SLF001 # type: ignore[reportPrivateUsage]
            logger.debug(reason, section_path=self.section_path_str)
            return True

        return False

    @contextmanager
    def start_file_section(
        self, file: Path | str, *, id: str | None = None, keep: bool = True, updated_at: datetime | None = None
    ) -> Iterator["FileSection"]:
        from dbnomics_fetcher_toolbox.sections.file_section import FileSection

        subsection = FileSection(
            downloader_helper=self._downloader_helper,
            fail_fast=self._fail_fast,
            file=file,
            id=id,
            keep=keep,
            parent_path=self.section_path,
            report_builder=self._report_builder,
            updated_at=updated_at,
            resume_mode=self._resume_mode,
        )
        success = yield from subsection._process()  # noqa: SLF001 # type: ignore[reportPrivateUsage]
        if success:
            self._file_subsections.append(subsection)

    @property
    def _cache_dir(self) -> Path:
        return self._downloader_helper._cache_dir  # noqa: SLF001 # type: ignore[reportPrivateUsage]

    @property
    def _debug_dir(self) -> Path:
        return self._downloader_helper.debug_dir  # type: ignore[reportPrivateUsage]

    def _process(self) -> Iterator[Self]:
        logger.debug("Start processing section %r", self.id, section_path=self.section_path_str)

        with Timer() as timer:
            try:
                yield self
            except Exception:
                if self._fail_fast:
                    raise
                logger.exception(
                    "Error processing section %r",
                    self.id,
                    duration=format_timer(timer),
                    section_path=self.section_path_str,
                )
                return

        if self._file_subsections:
            moved_files: list[Path] = []
            for file_subsection in self._file_subsections:
                did_move = file_subsection._finish()  # noqa: SLF001 # type: ignore[reportPrivateUsage]
                if did_move:
                    moved_files.append(file_subsection.file)
            logger.debug(
                "Moved files of subsections from cache dir to target dir: %s",
                format_csv_values(format_file_path_with_size(moved_file) for moved_file in moved_files),
                section_path=self.section_path_str,
            )

        logger.debug("Finished processing section %r", self.id, section_path=self.section_path_str)
