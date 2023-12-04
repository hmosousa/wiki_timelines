from src.scrape import _extract_paragraphs, scrape_entity
from src.utils import get_html


def test_extract_paragraphs():
    url = "https://en.wikipedia.org/wiki/Annexation_of_Crimea_by_the_Russian_Federation"
    html = get_html(url)
    paragraphs = _extract_paragraphs(html)
    assert isinstance(paragraphs[0], str)


def test_scrape_entity():
    result = scrape_entity(15920546)
    assert isinstance(result["start_time"], dict)
