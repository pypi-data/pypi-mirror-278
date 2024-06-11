import argparse
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Final, NoReturn, Self, TypeVar

from dbnomics_data_model.utils import parse_bool

from dbnomics_fetcher_toolbox._internal.argparse_utils import csv_section_ids, csv_str

if TYPE_CHECKING:
    from dbnomics_fetcher_toolbox.types import SectionId

EXCLUDE_OPTION_NAME: Final = "--exclude"
ONLY_OPTION_NAME: Final = "--only"
REPORT_FILE_OPTION_NAME: Final = "--report-file"


@dataclass(frozen=True, kw_only=True)
class BaseCLIArgs(ABC):
    exclude: list["SectionId"]
    fail_fast: bool
    log_format: str | None
    log_levels: list[str] | None
    only: list["SectionId"]
    report_file: Path | None
    resume: bool

    @classmethod
    @abstractmethod
    def parse(cls) -> Self: ...


TCLIArgs = TypeVar("TCLIArgs", bound=BaseCLIArgs)


class BaseCLIArgsParser:
    def __init__(self, *, args_class: type[TCLIArgs]) -> None:
        self.args_class = args_class
        self._argparse_parser = self.create_argparse_parser()

    def create_argparse_parser(self) -> argparse.ArgumentParser:
        argparse_parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        self.setup_argparse_parser(argparse_parser)
        return argparse_parser

    def fail(self, *, msg: str) -> NoReturn:
        self._argparse_parser.error(msg)

    def parse_args_namespace(self) -> argparse.Namespace:
        return self._argparse_parser.parse_args()

    def setup_argparse_parser(self, argparse_parser: argparse.ArgumentParser) -> None:
        argparse_parser.add_argument(
            "--fail-fast",
            action=argparse.BooleanOptionalAction,
            default=False if (v := os.getenv("TOOLBOX_FAIL_FAST")) is None else parse_bool(v),
            help="exit on first exception instead of just logging it",
        )
        argparse_parser.add_argument(
            "--log-format",
            default=os.getenv("TOOLBOX_LOG_FORMAT"),
            type=str,
            help="format of the log messages",
        )
        argparse_parser.add_argument(
            "--log-levels",
            default=os.getenv("TOOLBOX_LOG_LEVELS"),
            type=csv_str,
            help="Logging levels: logger_name1=log_level1,logger_name2=log_level2[,...]",
        )
        argparse_parser.add_argument(
            "--resume",
            action=argparse.BooleanOptionalAction,
            default=True if (v := os.getenv("TOOLBOX_RESUME")) is None else parse_bool(v),
            help="skip already downloaded resources",
        )

        selection_group = argparse_parser.add_mutually_exclusive_group()
        selection_group.add_argument(
            EXCLUDE_OPTION_NAME,
            default=os.getenv("TOOLBOX_EXCLUDE"),
            help="do not process the specified sections",
            metavar="SECTION_IDS",
            type=csv_section_ids,
        )
        selection_group.add_argument(
            ONLY_OPTION_NAME,
            default=os.getenv("TOOLBOX_ONLY"),
            help="process only the specified sections",
            metavar="SECTION_IDS",
            type=csv_section_ids,
        )
