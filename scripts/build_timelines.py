import json
import logging
from datetime import datetime
from pathlib import Path

from tqdm import tqdm

from src.process import ParagraphProcessor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://en.wikipedia.org/wiki/"

ROOT = Path(__file__).parent.parent


def get_temporal_entities(dirpath):
    tentities = {}
    for filepath in dirpath.glob("*json"):
        content = json.load(filepath.open())

        has_url = content["url"] is not None
        has_start_time = content["start_time"] is not None
        has_end_time = content["end_time"] is not None
        if (has_start_time or has_end_time) and has_url:
            url = content["url"]
            href = url.strip(BASE_URL)
            if href:
                tentities[href] = {
                    "id": content["id"],
                    "start_time": content["start_time"],
                    "end_time": content["end_time"],
                }
    return tentities


def collect_paragraphs(dirpath):
    paragraphs = []
    for filepath in dirpath.glob("*json"):
        content = json.load(filepath.open())
        if content["paragraphs"]:
            paragraphs += [
                {"dct": content["dct"], "text": p} for p in content["paragraphs"]
            ]
    return paragraphs


def build_timelines(paragraphs, temporal_entities):
    processor = ParagraphProcessor(temporal_entities)
    idx, timelines = 0, []
    for paragraph in tqdm(paragraphs):
        dct = datetime.fromisoformat(paragraph["dct"])
        text = paragraph["text"]
        result = processor(dct, text)
        if result:
            result["id"] = idx
            timelines.append(result)
            idx += 1
    return timelines


def main():
    entities_path = ROOT / "data" / "entities"

    temporal_entities = get_temporal_entities(entities_path)
    paragraphs = collect_paragraphs(entities_path)
    timelines = build_timelines(paragraphs, temporal_entities)

    opath = ROOT / "data" / "timelines.json"
    json.dump(timelines, opath.open("w"), indent=True)


if __name__ == "__main__":
    main()
