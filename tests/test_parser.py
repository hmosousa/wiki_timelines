from src.parser import extract_paragraphs
from src.utils import get_html


def test_extract_paragraphs():
    url = "https://en.wikipedia.org/wiki/Universe"
    html = get_html(url)
    paragraphs = extract_paragraphs(html)
    assert isinstance(paragraphs[0], str)
