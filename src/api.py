import logging
from abc import ABC

import requests

logger = logging.getLogger(__name__)


class API(ABC):
    def __init__(self) -> None:
        self.endpoint = None

    def _fetch(self, params: dict):
        result = requests.get(self.endpoint, params=params)
        if result.ok:
            return result.json()
        else:
            logger.warning(
                f"Failed to fetch entity {id} with status code {result.status_code}."
            )


class WikiData(API):
    def __init__(self) -> None:
        self.endpoint = "https://www.wikidata.org/w/api.php"

    def entity(self, id: int) -> dict:
        params = {
            "action": "wbgetentities",
            "ids": f"Q{id}",
            "format": "json",
            "languages": "en",
            "props": "info|aliases|claims",
        }
        return self._fetch(params)


class WikiPedia(API):
    def __init__(self) -> None:
        self.endpoint = "https://en.wikipedia.org/w/api.php"

    def page(self, pageid: int) -> dict:
        params = {
            "action": "parse",
            "pageid": pageid,
            "format": "json",
            "prop": "text",
            "redirects": "",
        }
        return self._fetch(params)
