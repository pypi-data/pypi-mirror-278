import daiquiri

from dbnomics_fetcher_toolbox.types import SectionId

__all__ = ["BaseSection"]

logger = daiquiri.getLogger(__name__)


class BaseSection:
    def __init__(
        self,
        *,
        fail_fast: bool,
        id: SectionId | str,
        parent_path: list[SectionId],
        resume_mode: bool,
    ) -> None:
        self.id = SectionId.parse(id)

        self._fail_fast = fail_fast
        self._parent_path = parent_path
        self._resume_mode = resume_mode

    @property
    def section_path(self) -> list[SectionId]:
        return [*self._parent_path, self.id]

    @property
    def section_path_str(self) -> str:
        return ".".join(self.section_path)
