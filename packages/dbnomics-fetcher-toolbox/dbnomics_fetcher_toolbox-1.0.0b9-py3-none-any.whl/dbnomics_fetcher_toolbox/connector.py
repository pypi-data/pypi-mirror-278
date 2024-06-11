from abc import ABC, abstractmethod
from collections.abc import Iterator
from typing import TYPE_CHECKING

from dbnomics_data_model.model import DatasetCode

if TYPE_CHECKING:
    from dbnomics_data_model.model import ProviderCode

    from dbnomics_fetcher_toolbox.helpers.converter_helper import ConverterHelper
    from dbnomics_fetcher_toolbox.helpers.downloader_helper import DownloaderHelper

__all__ = ["BaseConnector"]


class BaseConnector(ABC):
    def __init__(self, *, converter_helper: "ConverterHelper", downloader_helper: "DownloaderHelper") -> None:
        self._converter_helper = converter_helper
        self._downloader_helper = downloader_helper

    @abstractmethod
    def fetch_dataset(self, dataset_code: "DatasetCode") -> None: ...

    @abstractmethod
    def iter_dataset_codes(self) -> Iterator[DatasetCode]: ...

    @property
    @abstractmethod
    def provider_code(self) -> "ProviderCode": ...

    def start(self) -> None:  # noqa: B027
        pass
