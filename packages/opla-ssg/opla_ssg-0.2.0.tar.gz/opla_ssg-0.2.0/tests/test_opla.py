from opla import opla
import sys


def test_argparse():
    parser = opla.parse_args(["mdfile"])
    assert parser.mdfile is not None


def test_main(tmp_path):
    data = """---
title: Ma page perso
name: Joanna
occupation: Chargée de recherche
theme: 
    name: materialize
    color: teal
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
Section 2.2 content Section 2.2 content - Section 2.2 content"""

    with open(tmp_path / "test.md", "w") as f:
        f.write(data)
    file = tmp_path / "test.md"
    dir = tmp_path / "dirtest"
    sys.argv = ["opla", str(file), "-o", str(dir)]
    opla.main()
    assert (dir / "index.html").exists()
