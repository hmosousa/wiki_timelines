import json
import logging
from pathlib import Path

import fire

from src.meta import MAX_WIKIDATA_ID
from src.scrape import scrape_entity

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


ROOT = Path(__file__).parent.parent


def last_parsed_id(dirpath: Path):
    """Get the id of the last file that is on the dirpath (where the entities are being extracted)."""
    file_ids = [int(fp.stem[1:]) for fp in dirpath.glob("*.json")]
    if file_ids:
        return max(file_ids)
    else:
        return 1


def main(start_id: int = None, end_id: int = None):
    entities_path = ROOT / "data" / "entities"
    entities_path.mkdir(exist_ok=True, parents=True)

    if start_id is None:
        start_id = last_parsed_id(entities_path)

    if end_id is None:
        end_id = MAX_WIKIDATA_ID

    for entity_id in range(start_id, end_id):
        opath = entities_path / f"Q{entity_id}.json"
        if opath.exists():
            continue

        logger.info(f"Extracting entity {entity_id}.")
        result = scrape_entity(entity_id)

        if result:
            logger.info("Successfully parsed.")
            json.dump(result, opath.open("w"), indent=4)


if __name__ == "__main__":
    fire.Fire(main)
