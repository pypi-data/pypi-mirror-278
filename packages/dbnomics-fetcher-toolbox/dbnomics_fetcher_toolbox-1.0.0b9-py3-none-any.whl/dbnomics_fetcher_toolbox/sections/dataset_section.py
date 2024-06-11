from collections.abc import Iterator
from typing import TYPE_CHECKING, Self

import daiquiri
from contexttimer import Timer
from dbnomics_data_model.model import DatasetCode, DatasetId

from dbnomics_fetcher_toolbox._internal.formatters import format_timer
from dbnomics_fetcher_toolbox._internal.reports.convert_report_builder import ConvertReportBuilder
from dbnomics_fetcher_toolbox.sections.base_section import BaseSection
from dbnomics_fetcher_toolbox.sections.errors import DatasetNotConverted
from dbnomics_fetcher_toolbox.types import SectionId

if TYPE_CHECKING:
    from dbnomics_data_model.storage import StorageSession

    from dbnomics_fetcher_toolbox.helpers.converter_helper import ConverterHelper


__all__ = ["DatasetSection"]


logger = daiquiri.getLogger(__name__)


class DatasetSection(BaseSection):
    def __init__(
        self,
        *,
        converter_helper: "ConverterHelper",
        dataset_id: DatasetId,
        fail_fast: bool,
        id: SectionId | str | None,
        parent_path: list[SectionId],
        report_builder: ConvertReportBuilder,
        resume_mode: bool,
    ) -> None:
        if id is None:
            id = str(dataset_id.dataset_code)

        super().__init__(fail_fast=fail_fast, id=id, parent_path=parent_path, resume_mode=resume_mode)

        self._converter_helper = converter_helper
        self.dataset_id = dataset_id
        self._report_builder = report_builder

    @property
    def dataset_code(self) -> DatasetCode:
        return self.dataset_id.dataset_code

    @property
    def is_skipped(self) -> bool:
        reason = self._get_skip_reason()
        if reason is None:
            return False

        logger.debug(reason, section_path=self.section_path_str)
        self._report_builder.register_file_section_skip(self.id, message=reason)
        return True

    def _get_skip_reason(self) -> str | None:
        reason = self._converter_helper._is_section_skipped_for_options(self.id)  # noqa: SLF001 # type: ignore[reportPrivateUsage]
        if reason is not None:
            return reason

        return self._converter_helper._is_section_skipped_for_resume_mode(self.id, dataset_id=self.dataset_id)  # noqa: SLF001 # type: ignore[reportPrivateUsage]

    def _process(self) -> Iterator[tuple[Self, "StorageSession"]]:
        logger.debug("Start converting dataset %r", str(self.dataset_code), section_path=self.section_path_str)

        self._report_builder.register_dataset_section_start(self.id, dataset_code=self.dataset_code)

        is_skipped = self._get_skip_reason() is not None

        with (
            self._converter_helper.create_session(f"dataset-{self.dataset_code}") as session,
            Timer() as timer,
        ):
            try:
                yield self, session
            except Exception as exc:
                self._report_builder.register_dataset_section_failure(self.id, error=exc, timer=timer)
                if self._fail_fast:
                    raise
                logger.exception(
                    "Error converting dataset %r",
                    str(self.dataset_code),
                    duration=format_timer(timer),
                    section_path=self.section_path_str,
                )
                return False

            if not is_skipped:
                dataset_exists = session.storage.has_dataset(self.dataset_id)
                if not dataset_exists:
                    error = DatasetNotConverted(dataset_id=self.dataset_id, section_id=self.id)
                    message = str(error)
                    logger.error(message)
                    self._report_builder.register_dataset_section_failure(self.id, error=message, timer=timer)
                    return False

                session.commit()

        if not is_skipped:
            # Do not log or register a "success" after a "skip"...
            logger.debug(
                "Finished converting dataset %r successfully",
                str(self.dataset_code),
                duration=format_timer(timer),
                section_path=self.section_path_str,
            )
            self._report_builder.register_dataset_section_success(self.id, timer=timer)

        # ...but do not consider the skip as a failure.
        return True
