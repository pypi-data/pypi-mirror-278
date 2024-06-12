from opla import payload
import pytest
from pathlib import Path

def test_create_output_directory(tmp_path):
    dir = tmp_path / Path("output")
    payload.create_output_directory(dir)

    file = dir / "coco.txt"
    file.touch()

    payload.create_output_directory(dir)
    assert dir.exists()


class TestCopyFiles:
    @pytest.fixture
    def setup_dir(self, tmp_path):
        dir = payload.create_output_directory(tmp_path / Path("dir"))
        return dir

    def test_water(self, setup_dir):
        header = {"theme": {"name": "water"}}
        payload.copy_files(header, setup_dir)
        assert (Path(setup_dir) / "water/static").exists()

    def test_custom_list(self, setup_dir):
        header = {
            "theme": {
                "name": "rawhtml",
                "custom": [Path(__file__).parent / "data/css/index2.css"],
            }
        }
        payload.copy_files(header, setup_dir)
        assert (Path(setup_dir) / "custom/index2.css").exists()

    def test_custom_single(self, setup_dir):
        header = {
            "theme": {
                "name": "rawhtml",
                "custom": Path(__file__).parent / "data/css/index2.css",
            }
        }
        payload.copy_files(header, setup_dir)
        assert (Path(setup_dir) / "custom/index2.css").exists()

    def test_custom_dict_css_list(self, setup_dir):
        header = {
            "theme": {
                "name": "rawhtml",
                "custom": {"css": [Path(__file__).parent / "data/css/index2.css"]},
            }
        }
        payload.copy_files(header, setup_dir)
        assert (Path(setup_dir) / "custom/css/index2.css").exists()

    def test_custom_dict_css_single(self, setup_dir):
        header = {
            "theme": {
                "name": "rawhtml",
                "custom": {"css": Path(__file__).parent / "data/css/index2.css"},
            }
        }
        payload.copy_files(header, setup_dir)
        assert (Path(setup_dir) / "custom/css/index2.css").exists()

    def test_custom_dict_js_list(self, setup_dir):
        header = {
            "theme": {
                "name": "rawhtml",
                "custom": {
                    "js": [
                        Path(__file__).parent
                        / "data/js/bootstrap.min.js"
                    ]
                },
            }
        }
        payload.copy_files(header, setup_dir)
        assert (Path(setup_dir) / "custom/js/bootstrap.min.js").exists()

    def test_custom_dict_js_single(self, setup_dir):
        header = {
            "theme": {
                "name": "rawhtml",
                "custom": {
                    "js": Path(__file__).parent
                    / "data/js/bootstrap.min.js"
                },
            }
        }
        payload.copy_files(header, setup_dir)
        assert (Path(setup_dir) / "custom/js/bootstrap.min.js").exists()

    def test_materialize(self, setup_dir):
        header = {"theme": {"name": "materialize"}}
        payload.copy_files(header, setup_dir)
        assert (Path(setup_dir) / "materialize/static").exists()

    def test_data(self, setup_dir):
        header = {
            "theme": {"name": "rawhtml"},
            "data": [
                Path(__file__).parent / "data/img",
                Path(__file__).parent / "data/Resume.pdf",
            ],
        }
        payload.copy_files(header, setup_dir)
        assert Path(setup_dir / "img").exists()