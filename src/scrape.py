import logging

from bs4 import BeautifulSoup

from src.api import WikiData, WikiPedia
from src.meta import END_TIME_PID, START_TIME_PID
from src.utils import get_html

logger = logging.getLogger(__name__)


def _extract_paragraphs(html: str):
    """Extract paragraphs that contain links ot other wiki pages."""
    soup = BeautifulSoup(html, "html.parser")
    paragraphs = []
    for paragraph in soup.find_all("p"):
        if 'href="/wiki/' in str(paragraph):
            paragraphs.append(str(paragraph))
    return paragraphs


def _get_property(entity, property):
    if property in entity["claims"]:
        content = entity["claims"][property][0]
        try:
            value = content["mainsnak"]["datavalue"]["value"]
        except Exception as e:
            logger.info(e)
            # value = content
        return value


def scrape_entity(entity_id: int):
    """Scrape info of a given entity."""
    wikipedia_api = WikiPedia()
    wikidata_api = WikiData()

    entity = wikidata_api.entity(entity_id)
    if entity is not None:
        aliases = [a["value"] for a in entity["aliases"].get("en", [])]
        start_time = _get_property(entity, START_TIME_PID)
        end_time = _get_property(entity, END_TIME_PID)
        url = entity["sitelinks"].get("enwiki", {}).get("url")

        html = wikipedia_api.page(entity["pageid"])
        if html is None:
            html = get_html(url)

        paragraphs = None
        if html is not None:
            paragraphs = _extract_paragraphs(html)

        result = {
            "id": entity["id"],
            "title": entity["title"],
            "pageid": entity["pageid"],
            "url": url,
            "paragraphs": paragraphs,
            "dct": entity["modified"],
            "aliases": aliases,
            "start_time": start_time,
            "end_time": end_time,
        }
        return result
