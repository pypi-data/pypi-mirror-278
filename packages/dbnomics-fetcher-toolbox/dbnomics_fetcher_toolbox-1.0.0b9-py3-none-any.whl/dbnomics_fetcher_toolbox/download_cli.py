import argparse
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Self

import daiquiri
from dbnomics_data_model.utils import parse_bool

from dbnomics_fetcher_toolbox._internal.section_updates_repo import SECTION_UPDATES_FILE_NAME
from dbnomics_fetcher_toolbox.types import DownloaderHelperKwargsFromCli

from ._internal.base_cli import REPORT_FILE_OPTION_NAME, BaseCLIArgs, BaseCLIArgsParser

__all__ = ["DownloadCLIArgs", "DownloadCLIArgsParser"]

logger = daiquiri.getLogger(__name__)


@dataclass(frozen=True, kw_only=True)
class DownloadCLIArgs(BaseCLIArgs):
    cache_dir: Path | None
    debug_dir: Path | None
    incremental: bool
    target_dir: Path

    @classmethod
    def parse(cls) -> Self:
        parser = DownloadCLIArgsParser(args_class=cls)
        args_namespace = parser.parse_args_namespace()
        return cls(**vars(args_namespace))

    def as_downloader_helper_kwargs(self) -> DownloaderHelperKwargsFromCli:
        return {
            "cache_dir": self.cache_dir,
            "debug_dir": self.debug_dir,
            "excluded": self.exclude,
            "fail_fast": self.fail_fast,
            "incremental": self.incremental,
            "report_file": self.report_file,
            "resume_mode": self.resume,
            "selected": self.only,
            "target_dir": self.target_dir,
        }


class DownloadCLIArgsParser(BaseCLIArgsParser):
    def setup_argparse_parser(self, argparse_parser: argparse.ArgumentParser) -> None:
        super().setup_argparse_parser(argparse_parser)

        argparse_parser.add_argument("target_dir", type=Path, help="directory where provider data is written to")

        argparse_parser.add_argument(
            "--cache-dir",
            default=os.getenv("TOOLBOX_DOWNLOAD_CACHE_DIR"),
            help="directory where non-kept files can be written to (e.g. ZIP files)",
            type=Path,
        )
        argparse_parser.add_argument(
            "--debug-dir",
            default=os.getenv("TOOLBOX_DOWNLOAD_DEBUG_DIR"),
            help="directory where debug files can be written to (e.g. failed HTTP responses)",
            type=Path,
        )
        argparse_parser.add_argument(
            "--incremental",
            action=argparse.BooleanOptionalAction,
            default=True if (v := os.getenv("TOOLBOX_INCREMENTAL")) is None else parse_bool(v),
            help=f"only download sections newer than specified in {SECTION_UPDATES_FILE_NAME!r}",
        )
        argparse_parser.add_argument(
            REPORT_FILE_OPTION_NAME,
            default=os.getenv("TOOLBOX_DOWNLOAD_REPORT_FILE", default="download_report.json"),
            help="output file to write the error report to",
            type=Path,
        )
