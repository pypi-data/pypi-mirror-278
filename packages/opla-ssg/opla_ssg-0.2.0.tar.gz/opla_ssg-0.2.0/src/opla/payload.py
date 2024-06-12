"""Provide functions to copy static and attached files to output directory"""

import os
from pathlib import Path
import shutil

from .templating import TEMPLATES_PATH

def copy_files(header: dict, dst_dir: Path):
    """
    Copy static and attached files to a destination folder

    Args:
        header: the header of the markdown file
        dst_dir: the path to the destination folder
    """
    if "custom" in header["theme"]:
        if isinstance(header["theme"]["custom"], dict):
            if "css" in header["theme"]["custom"]:
                if isinstance(header["theme"]["custom"]["css"], list):
                    for file in header["theme"]["custom"]["css"]:
                        dir = dst_dir / "custom/css"
                        dir.mkdir(parents=True, exist_ok=True)
                        shutil.copy(file, dir)
                else:
                    dir = dst_dir / "custom/css"
                    dir.mkdir(parents=True, exist_ok=True)
                    shutil.copy(header["theme"]["custom"]["css"], dir)
            if "js" in header["theme"]["custom"]:
                if isinstance(header["theme"]["custom"]["js"], list):
                    for file in header["theme"]["custom"]["js"]:
                        dir = dst_dir / "custom/js"
                        dir.mkdir(parents=True, exist_ok=True)
                        shutil.copy(file, dir)
                else:
                    dir = dst_dir / "custom/js"
                    dir.mkdir(parents=True, exist_ok=True)
                    shutil.copy(header["theme"]["custom"]["js"], dir)
        else:
            if isinstance(header["theme"]["custom"], list):
                dir = dst_dir / "custom"
                dir.mkdir(exist_ok=True)
                for file in header["theme"]["custom"]:
                    shutil.copy(file, dir)
            else:
                dir = dst_dir / "custom"
                dir.mkdir(exist_ok=True)
                shutil.copy(header["theme"]["custom"], dir)

    if (header["theme"]["name"] == "water"):
        shutil.copytree(TEMPLATES_PATH / "water/static", dst_dir / "water/static")
    elif header["theme"]["name"] == "materialize":
        if not (dst_dir / "materialize/static").exists():
            shutil.copytree(TEMPLATES_PATH / "materialize/static", dst_dir / "materialize/static")

    if "data" in header:
        for file in header["data"]:
            if Path(file).is_dir():
                shutil.copytree(Path(file), dst_dir / Path(file).name)
            else:
                shutil.copy(Path(file), dst_dir)


def create_output_directory(dir: Path) -> Path:
    """
    Create the output directory if it doesn't exist, and remove then create it if it exists

    Args:
        dir: the path to the output directory

    Returns:
        Path: the created output directory
    """
    if dir.exists():
        shutil.rmtree(dir)
        dir.mkdir()
    else:
        os.makedirs(dir, exist_ok=True)

    return dir
