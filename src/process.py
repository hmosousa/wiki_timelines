import copy
import logging
from datetime import datetime

from bs4 import BeautifulSoup

from src.base import Instant, Relation
from src.utils import extract_date

logger = logging.getLogger(__name__)


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
                logger.warning(
                    f'Failed to parse date {ent["start_time"]} with error {e}'
                )

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
