"""Parse markdown file into header and sections and create menu from sections"""

from pathlib import Path
from typing import List, Tuple, Dict

import markdown  # type: ignore

from sgelt import mdparse
from sgelt.utils import parse_md_file
from .shortcodes import parser

md = markdown.Markdown(extensions=["toc", "attr_list"])


def convert_md_list_to_html(md_list: List[str]) -> List[str]:
    """
    Convert list of markdown content to list of HTML

    Args:
        md_list: a list of markdown content

    Returns:
        List[str]: a list of HTML content
    """
    # Remove <p> and </p> tags
    return [md.convert(md_element)[3:-4] for md_element in md_list]


def parse_markdown_file(mdfile_path: Path) -> Tuple[dict, list]:
    """
    Parse the markdown file into a header and a content

    Args:
        mdfile_path: Path to the markdown file

    Returns:
        Tuple[dict, list]: (header of the markdown file,
        content sections of the markdown file)
    """
    header, md_content = parse_md_file(mdfile_path)
    md_content = parser.parse(md_content)
    sections = mdparse.get_sections(md_content)

    try:
        header["theme"]["name"]
    except KeyError:  # Default theme
        header["theme"] = {"name": "water"}

    if "footer" in header:
        for key in header["footer"]:
            if key != "social":  # leave social list rendering to jinja templating
                # parse contact list or other lists
                header["footer"][key] = convert_md_list_to_html(header["footer"][key])
    return header, sections


def create_menu(sections: list[Dict]) -> list[Dict]:
    """
    Create a menu from a collection of sections

    Args:
        sections: Sections of the markdown with an id and a title

    Returns:
        List[Dict]: A list of menu items with a link href and a text
    """
    menu_links = []
    for section in sections[1:]:
        href = f"#{section['id']}"
        text = section["title"]
        menu_links.append({"href": href, "text": text})
    return menu_links
