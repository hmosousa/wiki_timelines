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
                f"Failed to fetch {params} with status code {result.status_code}."
            )


class WikiData(API):
    def __init__(self) -> None:
        self.endpoint = "https://www.wikidata.org/w/api.php"

    def entity(self, id_: int) -> dict:
        params = {
            "action": "wbgetentities",
            "ids": f"Q{id_}",
            "format": "json",
            "languages": "en",
            "props": "info|aliases|claims|sitelinks/urls",
            "sitefilter": "enwiki",
        }

        content = self._fetch(params)

        entity = None
        is_none = content is None
        is_error = "error" in content
        if not is_none and not is_error:
            content = content["entities"][f"Q{id_}"]
            if "missing" not in content:
                entity = content
        return entity


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

        content = self._fetch(params)

        page = None
        if "error" not in content:
            page = content["parse"]["text"]["*"]
        return page
