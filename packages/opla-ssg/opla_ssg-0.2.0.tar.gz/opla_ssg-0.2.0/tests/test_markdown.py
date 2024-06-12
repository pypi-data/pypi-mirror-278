from opla import markdown
import pytest
from pathlib import Path


@pytest.fixture
def theme():
    return "theme:\n    name: materialize"


class TestParseMarkdownFile:
    @pytest.fixture
    def setup_dir(self, tmp_path, theme) -> Path:
        """Create a markdown file with a header and sections for testing"""
        data = f"""\
---
title: Ma page perso
name: Erica
occupation: Chargée de recherche
{theme}
---

## Section 1

Section 1 content - Section 1 content Section 1 content - Section 1 content Section 1 content - Section 1 content
Section 1 content - Section 1 content
Section 1 content - Section 1 content

## Section 2

### Section 2.1

Section 2.1 content Section 2.1 content - Section 2.1 content

### Section 2.2

Section 2.2 content Section 2.2 content - Section 2.2 content
Section 2.2 content Section 2.2 content - Section 2.2 content

"""
        with open(tmp_path / "test.md", "w") as f:
            f.write(data)
        mdfilepath = tmp_path / Path("test.md")

        return mdfilepath

    @pytest.mark.parametrize("theme", ["theme:\n    name: materialize", ""])
    def test_parse_markdown_file_header(self, setup_dir, theme):
        header, _ = markdown.parse_markdown_file(setup_dir)

        expected = {
            "title": "Ma page perso",
            "name": "Erica",
            "occupation": "Chargée de recherche",
            "theme": {"name": "water"},
        }

        if theme == "":
            assert header == expected
        else:
            expected["theme"] = {"name": "materialize"}
            assert header == expected

    def test_parse_markdown_file_sections(self, setup_dir):
        _, sections = markdown.parse_markdown_file(setup_dir)

        assert len(sections) == 2


def test_create_menu(tmp_path):
    data = """---
title: Ma page perso
name: Joanna
occupation: Chargée de recherche
theme: 
    name: materialize
---
## Section 1

Section 1 content - Section 1 content Section 1 content - Section 1 content Section 1 content - Section 1 content
Section 1 content - Section 1 content
Section 1 content - Section 1 content

## Section 2

### Section 2.1

Section 2.1 content Section 2.1 content - Section 2.1 content

### Section 2.2

Section 2.2 content Section 2.2 content - Section 2.2 content
Section 2.2 content Section 2.2 content - Section 2.2 content

## Section 3

Section 3 content

"""

    with open(tmp_path / "test.md", "w") as f:
        f.write(data)

    mdfilepath = tmp_path / Path("test.md")
    _, (sections, _) = markdown.parse_markdown_file(mdfilepath)
    menu = markdown.create_menu(sections)

    assert menu == [
        {"href": "#section-2", "text": "Section 2"},
        {"href": "#section-3", "text": "Section 3"},
    ]


def test_convert_md_list_to_html():
    contact_markdown = [
        "<jlrda@dix-huitieme-siecle.fr>",
        "Six feet under the carrefour de Chateaudun-Place Kossuth, 75009 Paris, France",
        "+33 1 01 02 03 04",
    ]
    contact_html = markdown.convert_md_list_to_html(contact_markdown)
    expected = [
        '<a href="&#109;&#97;&#105;&#108;&#116;&#111;&#58;&#106;&#108;&#114;&#100;&#97;&#64;&#100;&#105;&#120;&#45;&#104;&#117;&#105;&#116;&#105;&#101;&#109;&#101;&#45;&#115;&#105;&#101;&#99;&#108;&#101;&#46;&#102;&#114;">&#106;&#108;&#114;&#100;&#97;&#64;&#100;&#105;&#120;&#45;&#104;&#117;&#105;&#116;&#105;&#101;&#109;&#101;&#45;&#115;&#105;&#101;&#99;&#108;&#101;&#46;&#102;&#114;</a>',
        "Six feet under the carrefour de Chateaudun-Place Kossuth, 75009 Paris, France",
        "+33 1 01 02 03 04",
    ]
    assert contact_html == expected
