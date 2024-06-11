from collections.abc import Generator
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any, Self

import daiquiri
from contexttimer import Timer
from humanfriendly.text import generate_slug

from dbnomics_fetcher_toolbox._internal.file_utils import move_file
from dbnomics_fetcher_toolbox._internal.formatters import format_timer
from dbnomics_fetcher_toolbox._internal.reports.download_report_builder import DownloadReportBuilder
from dbnomics_fetcher_toolbox.formatters import format_file_path_with_size
from dbnomics_fetcher_toolbox.sections.download_section import DownloadSection
from dbnomics_fetcher_toolbox.sections.errors import FileNotDownloaded
from dbnomics_fetcher_toolbox.types import SectionId

if TYPE_CHECKING:
    from dbnomics_fetcher_toolbox.helpers.downloader_helper import DownloaderHelper


__all__ = ["FileSection"]


logger = daiquiri.getLogger(__name__)


class FileSection(DownloadSection):
    def __init__(
        self,
        *,
        downloader_helper: "DownloaderHelper",
        fail_fast: bool,
        file: Path | str,
        id: SectionId | str | None,
        keep: bool,
        parent_path: list[SectionId],
        report_builder: DownloadReportBuilder,
        resume_mode: bool,
        updated_at: datetime | None,
    ) -> None:
        if id is None:
            id = generate_slug(str(file))

        super().__init__(
            downloader_helper=downloader_helper,
            fail_fast=fail_fast,
            id=id,
            parent_path=parent_path,
            report_builder=report_builder,
            resume_mode=resume_mode,
        )

        if isinstance(file, str):
            file = Path(file)
        if file.is_absolute():
            msg = f"file must be a relative path, got {str(file)!r}"
            raise ValueError(msg)
        self.relative_file = file

        self._finished = False
        self._keep = keep
        self._updated_at = updated_at

    @property
    def file(self) -> Path:
        return self._target_file if self._keep and self._finished else self._cache_file

    @property
    def is_skipped(self) -> bool:
        reason = self._get_skip_reason()
        if reason is None:
            return False

        logger.debug(reason, section_path=self.section_path_str)
        self._report_builder.register_file_section_skip(self.id, message=reason)
        return True

    @property
    def _cache_file(self) -> Path:
        return self._cache_dir / self.relative_file

    def _finish(self) -> bool:
        assert not self._finished
        did_move = False
        if self._keep and self._cache_file.is_file():
            move_file(self._cache_file, self._target_file)
            did_move = True
        self._finished = True
        return did_move

    def _get_skip_reason(self) -> str | None:
        reason = self._downloader_helper._is_section_skipped_for_options(self.id)  # noqa: SLF001 # type: ignore[reportPrivateUsage]
        if reason is not None:
            return reason

        resumed_source_file = self._target_file if self._keep else self._cache_file
        if self._resume_mode and resumed_source_file.is_file():
            return f"[Resume mode] Skipping section {self.id!r} because its associated file already exists: {format_file_path_with_size(resumed_source_file)}"  # noqa: E501

        return self._downloader_helper._is_section_skipped_for_incremental_mode(self.id, updated_at=self._updated_at)  # noqa: SLF001 # type: ignore[reportPrivateUsage]

    def _process(self) -> Generator[Self, Any, bool]:
        logger.debug("Start downloading file %r", str(self.relative_file), section_path=self.section_path_str)

        self._report_builder.register_file_section_start(self.id, file=self.relative_file)

        is_skipped = self._get_skip_reason() is not None

        with Timer() as timer:
            try:
                yield self
            except Exception as exc:
                self._report_builder.register_file_section_failure(self.id, error=exc, timer=timer)
                if self._fail_fast:
                    raise
                logger.exception(
                    "Error downloading file %s",
                    str(self.relative_file),
                    duration=format_timer(timer),
                    section_path=self.section_path_str,
                )
                return False

        if not is_skipped:
            if not self.file.is_file():
                error = FileNotDownloaded(file=self.relative_file, section_id=self.id)
                message = str(error)
                logger.error(message)
                self._report_builder.register_file_section_failure(self.id, error=message, timer=timer)
                return False

            # Do not log or register a "success" after a "skip"...
            logger.debug(
                "Finished downloading file %r successfully",
                str(self.relative_file),
                duration=format_timer(timer),
                section_path=self.section_path_str,
            )
            self._report_builder.register_file_section_success(self.id, timer=timer)

        # ...but do not consider the skip as a failure.
        return True

    @property
    def _target_file(self) -> Path:
        return self._downloader_helper.target_dir / self.relative_file
