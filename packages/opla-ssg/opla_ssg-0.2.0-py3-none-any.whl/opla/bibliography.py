"""Retrieve publications from HAL and handle publications list style format"""

from pybtex.backends.markdown import Backend  # type: ignore
from pybtex.style.sorting import BaseSortingStyle  # type: ignore
from typing import Dict, List
import json
from urllib import request
from pybtex.style.template import (  # type: ignore
    field,
    href,
    join,
    optional,
    sentence,
)
from pybtex.style.formatting.plain import Style  # type: ignore


class MyBackend(Backend):
    """Output the entry in a markdown list"""

    def write_entry(self, key, label, text):
        self.output(f"- {text}\n")


class MySortingStyle(BaseSortingStyle):
    """Sort entries by year in descending order"""

    def sorting_key(self, entry):
        return entry.fields["year"]

    def sort(self, entries):
        return sorted(entries, key=self.sorting_key, reverse=True)


class MyStyle(Style):
    """A custom class to display the HAL reference"""

    def format_web_refs(self, e):
        """Add HAL ref based on urlbst output.web.refs"""
        return sentence[
            optional[self.format_eprint(e)],
            optional[self.format_pubmed(e)],
            optional[self.format_doi(e)],
            optional[self.format_idhal(e)],
        ]

    def format_idhal(self, e):
        """Format HAL ref based on urlbst format.doi"""
        url = join[" https://hal.science/", field("hal_id", raw=True)]
        return href[url, join["hal:", field("hal_id", raw=True)]]


def get_publications(idhal: str) -> Dict[str, List[str]]:
    """
    Get the list of publications sorted by the document type, based on
    the IDHal of the author by questionning HAL

    Args:
        idhal: The id of the author

    Returns:
        dict: A dictionnary containing the publications retrieved
                  from the HAL API sorted by document type
    """
    url = (
        f"https://api.archives-ouvertes.fr/search/?q=authIdHal_s:{idhal}"
        "&wt=json&fl=docType_s,citationFull_s&rows=10000"
        r"&sort=publicationDate_tdate%20desc"
    )

    f = request.urlopen(url)
    jsondict = json.loads(f.read())

    pub_list = jsondict["response"]["docs"]
    # Create a {docType: [pub_str]} dictionnary
    pub_dict: Dict[str, List[str]] = {}
    for pub in pub_list:
        if pub["docType_s"] in pub_dict:  # pragma: no cover
            pub_dict[pub["docType_s"]].append(pub["citationFull_s"])  # pragma: no cover
        else:
            pub_dict[pub["docType_s"]] = [pub["citationFull_s"]]  # pragma: no cover
    return pub_dict
