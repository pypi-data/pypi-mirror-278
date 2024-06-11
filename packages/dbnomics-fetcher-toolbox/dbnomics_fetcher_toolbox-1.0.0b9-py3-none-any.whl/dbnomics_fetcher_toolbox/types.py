import re
from datetime import datetime
from pathlib import Path
from typing import Final, TypeAlias, TypedDict

from dbnomics_data_model.storage import Storage
from phantom.re import FullMatch

__all__ = ["DownloadSectionUpdates", "SectionId"]


section_id_regex: Final = re.compile(r"[\w-]+")


class SectionId(FullMatch, pattern=section_id_regex):
    __slots__ = ()


DownloadSectionUpdates: TypeAlias = dict[SectionId, datetime]


class BaseKwargsFromCli(TypedDict):
    excluded: list[SectionId] | None
    fail_fast: bool
    report_file: Path | None
    resume_mode: bool
    selected: list[SectionId] | None


class ConverterHelperKwargsFromCli(BaseKwargsFromCli):
    source_dir: Path
    target_storage: Storage


class DownloaderHelperKwargsFromCli(BaseKwargsFromCli):
    cache_dir: Path | None
    debug_dir: Path | None
    incremental: bool
    target_dir: Path
