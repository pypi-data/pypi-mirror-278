"""Handle shortcodes for generating publications list from HAL and from BibTeX files"""

import shortcodes  # type: ignore
import sys
from typing import Dict, List, Optional
from opla.bibliography import get_publications, MySortingStyle, MyBackend, MyStyle
from pybtex.plugin import find_plugin  # type: ignore
import io
import six  # type: ignore

HAL_PUBLICATIONS: Optional[Dict[str, List[str]]] = None

parser = shortcodes.Parser(start="{{%", end="%}}", esc="\\")


@shortcodes.register("publications_hal")
def publications_handler_hal(_, kwargs: dict, publications=None) -> str:
    """
    Generate a list of publications sorted by the document type

    Args:
        _: unused positional argument
        kwargs: keyword arguments
        publications: list of publications, None by default

    Returns:
        str: The list of the selected type of document publications
    """

    global HAL_PUBLICATIONS

    try:
        idhal = kwargs["idhal"]
    except KeyError:
        sys.exit("Publication shortcode: idhal is a required argument")

    try:
        doctype = kwargs["doctype"]
    except KeyError:
        sys.exit("Publication shortcode: doctype is a required argument")

    # Retrieve the publications from HAL if not already done
    # (use global variable to avoid multiple API requests)
    if HAL_PUBLICATIONS is None:
        HAL_PUBLICATIONS = get_publications(idhal)  # pragma: no cover
    try:
        publications = HAL_PUBLICATIONS[doctype]
        content = "\n- " + "\n- ".join(publications)
    except KeyError:
        raise KeyError(
            f"Publication shortcode: doctype {doctype} not found in HAL publications"
        )
    return content


@shortcodes.register("publications_bibtex")
def publications_handler_bibtex(_, kwargs: dict, __) -> str:
    """
    Generate a table of publications from a bibtex file

    Args:
        _: unused positional argument
        kwargs: keyword arguments
        __: unused context

    Returns:
        str: the list of the publications
    """

    file = kwargs["bibtex"]
    bib_parser = find_plugin("pybtex.database.input", "bibtex")
    bib_data = bib_parser().parse_file(file)

    style = MyStyle()
    style.sort = MySortingStyle().sort
    data_formatted = style.format_entries((six.itervalues(bib_data.entries)))
    output = io.StringIO()
    MyBackend().write_to_stream(data_formatted, output)

    return output.getvalue()


parser.register(publications_handler_hal, "publications_hal")
parser.register(publications_handler_bibtex, "publications_bibtex")
