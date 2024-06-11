from dataclasses import dataclass
from pathlib import Path

from dbnomics_data_model.model import DatasetId

from dbnomics_fetcher_toolbox.types import SectionId


@dataclass(frozen=True, kw_only=True)
class DatasetNotConverted:
    dataset_id: DatasetId
    section_id: SectionId

    def __str__(self) -> str:
        return f"Dataset {str(self.dataset_id)!r} was not converted by section {self.section_id!r}"


@dataclass(frozen=True, kw_only=True)
class FileNotDownloaded:
    file: Path
    section_id: SectionId

    def __str__(self) -> str:
        return f"Source data file {str(self.file)!r} was not downloaded by section {self.section_id!r}"
