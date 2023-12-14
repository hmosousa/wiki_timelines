import json
import logging
import multiprocessing as mp
import time
from pathlib import Path

import fire

from src.meta import MAX_WIKIDATA_ID
from src.scrape import scrape_entity

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


ROOT = Path(__file__).parent.parent
ENTITIES_PATH = ROOT / "data" / "entities"
ENTITIES_PATH.mkdir(exist_ok=True, parents=True)


def last_parsed_id(dirpath: Path) -> int:
    """Get the id of the last file that is on the dirpath (where the entities are being extracted)."""
    file_ids = [int(fp.stem[1:]) for fp in dirpath.glob("*.json")]
    if file_ids:
        return max(file_ids)
    else:
        return 1


def extract_and_store_entity(entity_id: int) -> None:
    opath = ENTITIES_PATH / f"Q{entity_id}.json"
    if not opath.exists():
        logger.info(f"Extracting entity {entity_id}.")
        try:
            result = scrape_entity(entity_id)

            if result:
                logger.info("Successfully parsed.")
                json.dump(result, opath.open("w"), indent=4)
                time.sleep(5)
        except Exception as e:
            logger.warning(f"Extraction of entity {entity_id} failed with error {e}")


def main(start_id: int = None, end_id: int = None):
    if start_id is None:
        start_id = last_parsed_id(ENTITIES_PATH)

    if end_id is None:
        end_id = MAX_WIKIDATA_ID

    ids = list(range(start_id, end_id))
    with mp.Pool() as executor:
        executor.map(extract_and_store_entity, ids)


if __name__ == "__main__":
    fire.Fire(main)
