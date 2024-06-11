import argparse
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Self

import daiquiri
from dbnomics_data_model.storage import Storage, StorageUri

from dbnomics_fetcher_toolbox._internal.argparse_utils import storage_uri
from dbnomics_fetcher_toolbox.types import ConverterHelperKwargsFromCli

from ._internal.base_cli import REPORT_FILE_OPTION_NAME, BaseCLIArgs, BaseCLIArgsParser

__all__ = ["ConvertCLIArgs", "ConvertCLIArgsParser"]


logger = daiquiri.getLogger(__package__)


@dataclass(frozen=True, kw_only=True)
class ConvertCLIArgs(BaseCLIArgs):
    source_dir: Path
    target_storage_uri: StorageUri

    @classmethod
    def parse(cls) -> Self:
        parser = ConvertCLIArgsParser(args_class=cls)
        args_namespace = parser.parse_args_namespace()
        return cls(**vars(args_namespace))

    def as_converter_helper_kwargs(self) -> ConverterHelperKwargsFromCli:
        target_storage = Storage.from_uri(self.target_storage_uri)
        return {
            "excluded": self.exclude,
            "fail_fast": self.fail_fast,
            "report_file": self.report_file,
            "resume_mode": self.resume,
            "selected": self.only,
            "source_dir": self.source_dir,
            "target_storage": target_storage,
        }


class ConvertCLIArgsParser(BaseCLIArgsParser):
    def setup_argparse_parser(self, argparse_parser: argparse.ArgumentParser) -> None:
        super().setup_argparse_parser(argparse_parser)

        argparse_parser.add_argument("source_dir", type=Path, help="directory where provider data is read from")
        argparse_parser.add_argument(
            "target_storage_uri",
            help="URI of the storage adapter used to write converted data (can be a director)",
            type=storage_uri,
        )

        argparse_parser.add_argument(
            REPORT_FILE_OPTION_NAME,
            default=os.getenv("TOOLBOX_CONVERT_REPORT_FILE", default="convert_report.json"),
            help="output file to write the error report to",
            type=Path,
        )
