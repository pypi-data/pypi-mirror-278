from collections.abc import Iterator
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from types import TracebackType
from typing import TYPE_CHECKING, Final, Self, TypeVar

import daiquiri

from dbnomics_fetcher_toolbox._internal.file_utils import create_directory
from dbnomics_fetcher_toolbox._internal.reports import DownloadReportBuilder
from dbnomics_fetcher_toolbox._internal.section_updates_repo import SectionUpdatesRepo
from dbnomics_fetcher_toolbox.formatters import format_file_path_with_size
from dbnomics_fetcher_toolbox.helpers.base_fetcher_helper import BaseFetcherHelper
from dbnomics_fetcher_toolbox.sections.download_section import DownloadSection
from dbnomics_fetcher_toolbox.sections.file_section import FileSection

if TYPE_CHECKING:
    from dbnomics_fetcher_toolbox.types import SectionId

__all__ = ["DownloaderHelper"]


logger = daiquiri.getLogger(__name__)


DEFAULT_CACHE_DIR_NAME: Final = ".cache"
DEFAULT_DEBUG_DIR_NAME: Final = ".debug"
DEFAULT_STATE_DIR_NAME: Final = ".state"

T = TypeVar("T")


class DownloaderHelper(BaseFetcherHelper):
    def __init__(
        self,
        *,
        cache_dir: Path | None = None,
        debug_dir: Path | None = None,
        excluded: list["SectionId"] | None = None,
        fail_fast: bool = False,
        incremental: bool = True,
        report_file: Path | None = None,
        resume_mode: bool = True,
        selected: list["SectionId"] | None = None,
        target_dir: Path,
    ) -> None:
        super().__init__(
            excluded=excluded,
            fail_fast=fail_fast,
            report_file=report_file,
            resume_mode=resume_mode,
            selected=selected,
        )

        if cache_dir is None:
            cache_dir = target_dir / Path(DEFAULT_CACHE_DIR_NAME)
        self._cache_dir = cache_dir

        if debug_dir is None:
            debug_dir = target_dir / Path(DEFAULT_DEBUG_DIR_NAME)
        self.debug_dir = debug_dir

        self._incremental = incremental
        self._state_dir = target_dir / Path(DEFAULT_STATE_DIR_NAME)
        self.target_dir = target_dir

        self._report_builder = DownloadReportBuilder()
        self._section_updates_repo = SectionUpdatesRepo(base_dir=self._state_dir)

        self._create_directories()

    def __enter__(self) -> Self:
        self._section_updates_repo.load()
        return self

    def __exit__(
        self, exc_type: type[BaseException] | None, exc: BaseException | None, traceback: TracebackType | None
    ) -> None:
        if exc_type is None:
            self._log_unmatched_filters()
            self._save_report()
            self._section_updates_repo.save()
            self._log_stats()

    @contextmanager
    def start_file_section(
        self, file: Path | str, *, id: str | None = None, keep: bool = True, updated_at: datetime | None = None
    ) -> Iterator[FileSection]:
        section = FileSection(
            downloader_helper=self,
            fail_fast=self._fail_fast,
            file=file,
            id=id,
            keep=keep,
            parent_path=[],
            report_builder=self._report_builder,
            resume_mode=self._resume_mode,
            updated_at=updated_at,
        )

        if updated_at is not None:
            self._section_updates_repo.set_updated_at(section.id, updated_at=updated_at)

        is_ok = yield from section._process()  # noqa: SLF001 # type: ignore[reportPrivateUsage]
        if is_ok:
            did_move = section._finish()  # noqa: SLF001 # type: ignore[reportPrivateUsage]
            if did_move:
                logger.debug(
                    "Moved file from cache dir to target dir: %s",
                    format_file_path_with_size(section.file),
                    section_path=section.section_path_str,
                )

    @contextmanager
    def start_section(self, id: str) -> Iterator[DownloadSection]:
        section = DownloadSection(
            downloader_helper=self,
            fail_fast=self._fail_fast,
            id=id,
            parent_path=[],
            resume_mode=self._resume_mode,
            report_builder=self._report_builder,
        )
        yield from section._process()  # noqa: SLF001 # type: ignore[reportPrivateUsage]

    def _create_directories(self) -> None:
        create_directory(self._cache_dir, kind="cache", with_gitignore=True)
        create_directory(self.debug_dir, kind="debug", with_gitignore=True)
        create_directory(self._state_dir, kind="state", with_gitignore=True)
        create_directory(self.target_dir, kind="target")

    def _get_report_builder(self) -> DownloadReportBuilder:
        return self._report_builder

    def _is_section_skipped_for_incremental_mode(
        self, section_id: "SectionId", *, updated_at: datetime | None
    ) -> str | None:
        if updated_at is None or not self._incremental:
            return None

        last_updated_at = self._section_updates_repo.get_updated_at(section_id)
        if last_updated_at is None:
            return None

        if last_updated_at > updated_at:
            logger.warning(
                "[Incremental mode] Last update date %r of section %r is more recent than the new one %r, ignoring invalid value and processing section",  # noqa: E501
                last_updated_at.isoformat(),
                section_id,
                updated_at.isoformat(),
            )
            return None

        if updated_at > last_updated_at:
            logger.debug(
                "[Incremental mode] Processing section %r because the new update date %r is more recent than the last one %r",  # noqa: E501
                section_id,
                updated_at.isoformat(),
                last_updated_at.isoformat(),
            )
            return None

        assert updated_at == last_updated_at
        return f"[Incremental mode] Skipping section {section_id!r} because the last update date is the same as the new one: {updated_at.isoformat()}"  # noqa: E501
