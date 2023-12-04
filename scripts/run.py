import json
import logging
from pathlib import Path

from src.api import WikiData, WikiPedia
from src.parser import extract_paragraphs
from src.utils import get_html

logger = logging.getLogger(__name__)

MAX_ID = 99999999
START_TIME_PID = "P580"
END_TIME_PID = "P582"

ROOT = Path(__file__).parent.parent


def main():
    entities_path = ROOT / "data" / "entities"

    wikidata_api = WikiData()
    wikipedia_api = WikiPedia()
    for id_ in range(MAX_ID):
        opath = entities_path / f"Q{id_}.json"
        if opath.exists():
            continue

        print(id_)
        entity = wikidata_api.entity(id_)

        if entity is not None:
            aliases = [a["value"] for a in entity["aliases"].get("en", [])]
            start_time = entity["aliases"].get(START_TIME_PID)
            end_time = entity["aliases"].get(END_TIME_PID)
            url = entity["sitelinks"].get("enwiki", {"url": None})["url"]

            html = wikipedia_api.page(entity["pageid"])
            if html is None:
                html = get_html(url)

            paragraphs = None
            if html is not None:
                paragraphs = extract_paragraphs(html)

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

            json.dump(result, opath.open("w"), indent=4)


if __name__ == "__main__":
    main()
