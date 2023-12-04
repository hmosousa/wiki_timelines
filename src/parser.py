from bs4 import BeautifulSoup


def extract_paragraphs(html: str):
    soup = BeautifulSoup(html, "html.parser")
    paragraphs = []
    for paragraph in soup.find_all("p"):
        if paragraph.text.strip():
            paragraphs.append(str(paragraph))
    return paragraphs
