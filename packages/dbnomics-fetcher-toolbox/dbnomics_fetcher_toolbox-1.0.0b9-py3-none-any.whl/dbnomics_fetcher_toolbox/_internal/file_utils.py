from pathlib import Path

import daiquiri
from dbnomics_data_model.file_utils import write_gitignore_all

logger = daiquiri.getLogger(__name__)


def create_directory(directory: Path, *, kind: str, with_gitignore: bool = False) -> None:
    if directory.is_dir():
        logger.debug("Using the existing directory %r as the %s directory", str(directory), kind)
        return
    try:
        directory.mkdir(exist_ok=True, parents=True)
    except OSError as exc:
        from dbnomics_fetcher_toolbox.errors.downloader_helper import DirectoryCreateError

        raise DirectoryCreateError(directory, kind=kind) from exc

    if with_gitignore:
        write_gitignore_all(directory, exist_ok=True)

    logger.debug("Created %s directory: %r", kind, str(directory))


def is_directory_empty(directory: Path) -> bool:
    return not any(directory.iterdir())


def move_file(src: Path, dest: Path) -> None:
    dest.parent.mkdir(exist_ok=True, parents=True)
    src.rename(dest)


def replace_all_extensions(file: Path, extensions: list[str]) -> Path:
    return file.with_name(file.name.split(".")[0]).with_suffix("".join(extensions))
