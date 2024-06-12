from opla import shortcodes
import pytest

class TestPublicationsHandlerHal:
    @pytest.fixture
    def setup_pub(self):
        pub = shortcodes.HAL_PUBLICATIONS = {"ART": ["Example of ART publication text"]}
        yield pub

    def test_no_idhal(self, setup_pub):
        kwargs = {"doctype": "ART"}

        with pytest.raises(SystemExit) as exception:
            shortcodes.publications_handler_hal(None, kwargs, setup_pub)

        assert (
            exception.value.args[0]
            == "Publication shortcode: idhal is a required argument"
        )

    def test_no_doctype(self, setup_pub):
        kwargs = {"idhal": "idhal"}

        with pytest.raises(SystemExit) as exception:
            shortcodes.publications_handler_hal(None, kwargs, setup_pub)

        assert (
            exception.value.args[0]
            == "Publication shortcode: doctype is a required argument"
        )

    def test_unknown_doctype(self, setup_pub):
        kwargs = {"idhal": "idhal", "doctype": "PUB"}

        with pytest.raises(KeyError) as exception:
            shortcodes.publications_handler_hal(None, kwargs, setup_pub)

        assert (
            exception.value.args[0]
            == f"Publication shortcode: doctype {kwargs['doctype']} not found in HAL publications"
        )

    def test_publications_handler(self, setup_pub):
        kwargs = {"idhal": "idhal", "doctype": "ART"}
        content = shortcodes.publications_handler_hal(None, kwargs, setup_pub)

        assert "Example of ART publication text" in content


def test_publications_handler_bibtex(tmp_path):
    data = """
            @article{heu:hal-03546417,
  TITLE = {{Holomorphic Connections on Filtered Bundles over Curves}},
  AUTHOR = {Heu, Viktoria and Biswas, Indranil},
  URL = {https://hal.science/hal-03546417},
  JOURNAL = {{Documenta Mathematica}},
  PUBLISHER = {{Universit{\"a}t Bielefeld}},
  YEAR = {2013},
  KEYWORDS = {2010 Mathematics Subject Classification: 14H60 ; 14F05 ; 53C07 Keywords and Phrases: Holomorphic connection ; filtration ; Atiyah bundle ; parabolic subgroup},
  HAL_ID = {hal-03546417},
  HAL_VERSION = {v1},
}
            """
    with open(tmp_path / "test.html", "w") as f:
        f.write(data)

    file = tmp_path / "test.html"

    kwargs = {"bibtex": file}
    res = shortcodes.publications_handler_bibtex(None, kwargs, None)

    assert "Holomorphic Connections on Filtered Bundles over Curves" in res