"""
Main module for the opla package
"""

import argparse
from pathlib import Path
import sys


from .payload import create_output_directory, copy_files
from .markdown import parse_markdown_file, create_menu
from .templating import get_template



def parse_args(args: list) -> argparse.Namespace:
    """
    Console script for opla

    Args:
        args: the list of the command-line arguments

    Returns:
        argparse.Namespace: an object containing the parsed arguments
    """
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("mdfile", type=Path, help="markdown file path")
    parser.add_argument(
        "-o", "--output", type=Path, default=Path("build"), help="output directory"
    )

    return parser.parse_args(args)


def main():
    """
    Generates a personal page by parsing command-line arguments, creating the page content and its menu, renders the HTML template, and writes the result into a HTML file
    """
    args = parse_args(sys.argv[1:])

    output_directory_path = args.output

    create_output_directory(output_directory_path)

    header, (sections, _) = parse_markdown_file(args.mdfile)
    menu = create_menu(sections)

    copy_files(header, output_directory_path)

    template = get_template(header)
    html_out = template.render(
        sections=sections,
        header=header,
        menu=menu,
        output=output_directory_path,
        color=header["theme"].get("color")
    )

    with open(output_directory_path / "index.html", "w") as f:
        f.write(html_out)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
