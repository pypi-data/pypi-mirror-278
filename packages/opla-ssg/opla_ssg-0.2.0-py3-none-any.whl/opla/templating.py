"""Provide a function to get the jinja template."""

from pathlib import Path

import jinja2


TEMPLATES_PATH = Path(__file__).parent / "themes"


def get_template(header: dict) -> jinja2.Template:
    """
    Get the appropriate template according to the theme name

    Args:
        header: the header of the markdown file

    Returns:
        jinja2.Template: the requested template
    """

    env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATES_PATH))

    theme = header["theme"]["name"]
    if theme == "rawhtml":
        template = env.get_template("base/templates/base.html.j2")
    elif theme == "water":
        template = env.get_template("water/templates/index.html.j2")
    elif theme == "materialize":
        template = env.get_template("materialize/templates/index.html.j2")
        # Add default color to theme
        color = header["theme"].get("color", "teal")
        header["theme"]["color"] = color
    else:
        raise ValueError(f"Unknown theme name: '{theme}'")
    return template
