from collections.abc import Iterator
from typing import TYPE_CHECKING, Self

import daiquiri
from contexttimer import Timer

from dbnomics_fetcher_toolbox._internal.formatters import format_timer
from dbnomics_fetcher_toolbox.sections.base_section import BaseSection
from dbnomics_fetcher_toolbox.types import SectionId

if TYPE_CHECKING:
    from dbnomics_data_model.storage import StorageSession

    from dbnomics_fetcher_toolbox.helpers.converter_helper import ConverterHelper


__all__ = ["ConvertSection"]


logger = daiquiri.getLogger(__name__)


class ConvertSection(BaseSection):
    def __init__(
        self,
        *,
        converter_helper: "ConverterHelper",
        fail_fast: bool,
        id: SectionId | str,
        parent_path: list[SectionId],
        resume_mode: bool,
    ) -> None:
        super().__init__(fail_fast=fail_fast, id=id, parent_path=parent_path, resume_mode=resume_mode)
        self._converter_helper = converter_helper

    @property
    def is_skipped(self) -> bool:
        if reason := self._converter_helper._is_section_skipped_for_options(self.id):  # noqa: SLF001 # type: ignore[reportPrivateUsage]
            logger.debug(reason, section_path=self.section_path_str)
            return True

        return False

    def _process(self) -> Iterator[tuple[Self, "StorageSession"]]:
        logger.debug("Start processing section %r", self.id, section_path=self.section_path_str)

        with (
            self._converter_helper.create_session(self.id) as session,
            Timer() as timer,
        ):
            try:
                yield self, session
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

        logger.debug("Finished processing section %r", self.id, section_path=self.section_path_str)
