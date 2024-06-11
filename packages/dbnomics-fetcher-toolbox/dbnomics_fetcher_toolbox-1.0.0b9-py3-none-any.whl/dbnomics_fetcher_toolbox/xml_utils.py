import os
import subprocess
from collections.abc import Iterable, Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import TYPE_CHECKING

import daiquiri
from contexttimer import Timer
from iterable_subprocess import iterable_subprocess
from lxml import etree

from dbnomics_fetcher_toolbox._internal.formatters import format_timer
from dbnomics_fetcher_toolbox.formatters import format_file_path_with_size

if TYPE_CHECKING:
    from lxml._types import _TagSelector  # type: ignore[reportPrivateUsage]
    from lxml.etree import _Element  # type: ignore[reportPrivateUsage]
    from lxml.etree._iterparse import _NoNSEventNames  # type: ignore[reportPrivateUsage]

__all__ = ["fast_iter", "iter_xml_elements", "reformat_xml_file", "reformat_xml_stream"]


logger = daiquiri.getLogger(__name__)


def fast_iter(context: "etree.iterparse[tuple[_NoNSEventNames, _Element]]") -> Iterator[tuple[str, "_Element"]]:
    """Iterate the elements of context keeping memory usage low.

    See Also
    --------
    - http://stackoverflow.com/a/12161078
    - based on Liza Daly's fast_iter https://web.archive.org/web/20210309115224/http://www.ibm.com/developerworks/xml/library/x-hiperfparse/ # noqa

    """
    for event, element in context:
        yield event, element
        # It's safe to call clear() here because no descendants will be accessed
        element.clear()
        # Also eliminate now-empty references from the root node to element
        for ancestor in element.xpath("ancestor-or-self::*"):
            while ancestor.getprevious() is not None:
                del ancestor.getparent()[0]
    del context


def iter_xml_elements(
    xml_file: Path, *, huge_tree: bool = True, tag: "_TagSelector | Iterable[_TagSelector]"
) -> Iterator["_Element"]:
    context = etree.iterparse(xml_file, events=["end"], huge_tree=huge_tree, tag=tag)
    for _, element in fast_iter(context):
        yield element


def reformat_xml_file(xml_file: Path, *, indent_level: int = 2) -> None:
    tmp_file = xml_file.with_suffix(".tmp.xml")
    with Timer() as timer:
        try:
            output = subprocess.check_output(
                [  # noqa: S603
                    os.getenv("XMLINDENT_PATH", default="/usr/bin/xmlindent"),
                    "-i",
                    str(indent_level),
                    str(xml_file),
                    "-o",
                    str(tmp_file),
                ],
                stderr=subprocess.PIPE,
            )
        except subprocess.CalledProcessError as exc:
            logger.error("Error reformatting XML file, xmlindent stderr: %s", exc.stderr.decode("utf-8"))  # noqa: TRY400
            raise
    tmp_file.rename(xml_file)
    stdout = output.decode("utf-8")
    log_msg = "Reformatted XML file %s"
    if stdout:
        log_msg += f"xmlindent stdout: {stdout}"
    logger.debug(
        log_msg,
        format_file_path_with_size(xml_file),
        duration=format_timer(timer),
    )


@contextmanager
def reformat_xml_stream(xml_chunks: Iterator[bytes], *, indent_level: int = 2) -> Iterator[Iterator[bytes]]:
    with iterable_subprocess(
        [
            os.getenv("XMLINDENT_PATH", default="/usr/bin/xmlindent"),
            "-f",  # force indenting elements without children
            "-i",
            str(indent_level),
        ],
        xml_chunks,
    ) as output:
        yield output
