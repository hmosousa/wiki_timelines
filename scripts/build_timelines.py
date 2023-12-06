import copy
import json
import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from bs4 import BeautifulSoup
from tqdm import tqdm

from src.utils import extract_date

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


@dataclass
class Instant:
    id: str
    value: datetime
    start: bool = False
    end: bool = False

    def __str__(self) -> str:
        if self.start:
            return f"start {self.id}"
        elif self.end:
            return f"end {self.id}"
        else:
            return self.id


@dataclass
class Relation:
    source: Instant
    target: Instant

    @property
    def value(self):
        if self.source.value < self.target.value:
            return "<"
        elif self.source.value > self.target.value:
            return ">"
        else:
            return "="

    def to_dict(self):
        return {
            "source": str(self.source),
            "target": str(self.target),
            "relation": self.value,
        }


class ParagraphProcessor:
    def __init__(self, entities: dict) -> None:
        self._entities = entities

    def __call__(self, dct: datetime, text: str):
        """Process the paragraph to only include temporal entities."""
        soup, t_ents = self._process_text(text)
        if t_ents:
            context = self._build_context(dct, soup)
            instants = self._compile_instants(dct, t_ents)
            timeline = self._build_timeline(instants)
            if timeline:
                result = {
                    "context": context,
                    "entities": [str(inst) for inst in instants],
                    "timeline": timeline,
                }
                return result

    def _build_context(self, dct, soup):
        dct_str = dct.strftime("%m/%d/%Y, %H:%M:%S")
        context = f"Documents Creation Time: <t0>{dct_str}</t0>\n{soup}"
        return context

    def _compile_instants(self, dct, entities):
        instants = [Instant("t0", dct)]
        for ent in entities:
            try:
                start_time = extract_date(ent["start_time"]["time"], start=True)
                start_inst = Instant(ent["id"], start_time, start=True)
                instants.append(start_inst)
            except Exception as e:
                logger.warning(f'Failed to parse date {ent["start_time"]} with error {e}')

            try:
                end_time = extract_date(ent["end_time"]["time"], end=True)
                end_inst = Instant(ent["id"], end_time, end=True)
                instants.append(end_inst)
            except Exception as e:
                logger.warning(f'Failed to parse date {ent["end_time"]} with error {e}')
        return instants

    def _build_timeline(self, instants: list[Instant]):
        timeline = []
        insts = copy.deepcopy(instants)
        while insts:
            src = insts.pop(0)
            for tgt in insts:
                relation = Relation(src, tgt)
                timeline.append(relation.to_dict())
        return timeline

    def _process_text(self, text):
        soup = BeautifulSoup(text, features="html.parser")
        idx, t_ents = 0, []
        for ent in soup.find_all():
            href = None
            if "href" in ent.attrs:
                href = ent.attrs["href"].strip("/wiki/")

            if href in self._entities:
                ent_id = f"e{idx}"
                ent.name = ent_id
                ent.attrs = {}

                t_ent = self._entities[href]
                t_ent["id"] = ent_id
                t_ents.append(t_ent)

                idx += 1
            else:
                ent.unwrap()

        return soup, t_ents


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

    opath = ROOT / 'data' / 'timelines.json'
    json.dump(timelines, opath.open('w'), indent=True)


if __name__ == "__main__":
    main()
