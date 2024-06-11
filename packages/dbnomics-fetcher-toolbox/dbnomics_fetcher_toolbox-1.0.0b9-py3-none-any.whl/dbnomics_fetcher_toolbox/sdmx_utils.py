from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lxml.etree import _Element  # type: ignore[reportPrivateUsage]


__all__ = ["normalize_header_element", "sdmx_namespaces"]


sdmx_namespaces = {
    "com": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common",
    "data": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/structurespecific",
    "footer": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message/footer",
    "gen": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic",
    "md": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/metadata/generic",
    "mes": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message",
    "str": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure",
    "xml": "http://www.w3.org/XML/1998/namespace",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
}


def normalize_header_element(header_element: "_Element") -> None:
    """Modify header_element normalizing children that change too often.

    This is specifically useful to avoid creating a false revision of the file.
    """
    for tag_name, new_value in [("mes:ID", "IDREF111"), ("mes:Prepared", "1111-11-11T11:11:11")]:
        child_element = header_element.find(tag_name, namespaces=sdmx_namespaces)
        if child_element is not None:
            child_element.text = new_value
