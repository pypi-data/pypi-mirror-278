from datetime import datetime
from pathlib import Path
from typing import Final

import daiquiri
from dbnomics_data_model.json_utils import dump_as_json_bytes, parse_json_bytes, parse_json_data
from typedload.datadumper import Dumper
from typedload.dataloader import Loader

from dbnomics_fetcher_toolbox.formatters import format_file_path_with_size
from dbnomics_fetcher_toolbox.types import DownloadSectionUpdates, SectionId

SECTION_UPDATES_FILE_NAME: Final = "updates.json"

logger = daiquiri.getLogger(__name__)


class SectionUpdatesRepo:
    def __init__(self, *, base_dir: Path) -> None:
        self._base_dir = base_dir

        self._dumper = self._create_dumper()
        self._loader = self._create_loader()
        self._section_updates: DownloadSectionUpdates = {}

    def get_updated_at(self, section_id: SectionId) -> datetime | None:
        return self._section_updates.get(section_id)

    def load(self) -> None:
        section_updates_file = self._section_updates_file
        if not section_updates_file.is_file():
            logger.debug("[Incremental mode] is disabled because %r does not exist", str(section_updates_file))
            return

        section_updates_bytes = section_updates_file.read_bytes()
        section_updates_data = parse_json_bytes(section_updates_bytes)
        self._section_updates = parse_json_data(section_updates_data, loader=self._loader, type_=DownloadSectionUpdates)
        logger.debug(
            "[Incremental mode] is enabled, loaded section updates from %s",
            format_file_path_with_size(section_updates_file),
        )

    def save(self) -> None:
        section_updates_file = self._section_updates_file
        section_updates_bytes = dump_as_json_bytes(self._section_updates, dumper=self._dumper)
        section_updates_file.write_bytes(section_updates_bytes)
        logger.info("Section updates saved to %s", format_file_path_with_size(section_updates_file))

    def set_updated_at(self, section_id: SectionId, *, updated_at: datetime) -> None:
        self._section_updates[section_id] = updated_at

    def _create_dumper(self) -> Dumper:
        dumper = Dumper(hidedefault=False, isodates=True)
        dumper.strconstructed.add(SectionId)  # type: ignore[reportUnknownMemberType]
        return dumper

    def _create_loader(self) -> Loader:
        loader = Loader()
        loader.strconstructed.add(SectionId)  # type: ignore[reportUnknownMemberType]
        return loader

    @property
    def _section_updates_file(self) -> Path:
        return self._base_dir / SECTION_UPDATES_FILE_NAME
