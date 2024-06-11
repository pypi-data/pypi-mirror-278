"""Logging utility functions."""

import logging
from collections.abc import Iterable
from typing import Final

import daiquiri
from daiquiri.formatter import ColorExtrasFormatter
from daiquiri.output import Stream
from dbnomics_data_model.model import ProviderCode
from dotenv import find_dotenv, load_dotenv

from dbnomics_fetcher_toolbox.convert_cli import ConvertCLIArgs
from dbnomics_fetcher_toolbox.download_cli import DownloadCLIArgs
from dbnomics_fetcher_toolbox.helpers.converter_helper import ConverterHelper
from dbnomics_fetcher_toolbox.helpers.downloader_helper import DownloaderHelper

__all__ = [
    "create_converter_helper",
    "create_downloader_helper",
    "init_convert_cli",
    "init_download_cli",
    "load_env_variables_from_file",
    "setup_logging",
]


DEFAULT_LOGGING_FORMAT: Final = "%(asctime)s %(color)s%(levelname)-8.8s %(name)s: %(message)s%(extras)s%(color_stop)s"


def create_converter_helper(*, package_name: str, provider_code: ProviderCode | str) -> ConverterHelper:
    args = init_convert_cli(package_name=package_name)
    return ConverterHelper(provider_code=provider_code, **args.as_converter_helper_kwargs())


def create_downloader_helper(*, package_name: str) -> DownloaderHelper:
    args = init_download_cli(package_name=package_name)
    return DownloaderHelper(**args.as_downloader_helper_kwargs())


def init_convert_cli(*, package_name: str) -> ConvertCLIArgs:
    load_env_variables_from_file()
    args = ConvertCLIArgs.parse()
    setup_logging(log_format=args.log_format, log_levels=args.log_levels, package_name=package_name)
    return args


def init_download_cli(*, package_name: str) -> DownloadCLIArgs:
    load_env_variables_from_file()
    args = DownloadCLIArgs.parse()
    setup_logging(log_format=args.log_format, log_levels=args.log_levels, package_name=package_name)
    return args


def load_env_variables_from_file() -> None:
    load_dotenv(find_dotenv(usecwd=True))


def setup_logging(*, log_format: str | None = None, log_levels: Iterable[str] | None = None, package_name: str) -> None:
    """Setup logging using the provided log format and log level."""  # noqa: D401
    if log_format is None:
        log_format = DEFAULT_LOGGING_FORMAT

    daiquiri.setup(
        outputs=[
            Stream(formatter=ColorExtrasFormatter(fmt=log_format)),
        ],
    )

    if log_levels is None:
        daiquiri.set_default_log_levels(
            [
                ("__main__", logging.DEBUG),
                ("dbnomics_data_model", logging.DEBUG),
                ("dbnomics_fetcher_toolbox", logging.DEBUG),
                (package_name, logging.DEBUG),
            ]
        )
    else:
        daiquiri.parse_and_set_default_log_levels(log_levels)
