from opla import bibliography

def test_publications():
    publications = bibliography.get_publications("idHal")
    assert isinstance(publications, dict)