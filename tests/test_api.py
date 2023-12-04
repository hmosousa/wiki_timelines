from src.api import WikiData, WikiPedia


class TestWikiData:
    api = WikiData()

    def test_entity(self):
        entity = self.api.entity(15920546)
        assert entity['id'] == "Q15920546"

    def test_invalid_entity(self):
        entity = self.api.entity(159205460)
        assert entity is None


class TestWikiPedia:
    api = WikiPedia()

    def test_page(self):
        html = self.api.page(17545100)
        assert isinstance(html, str)

    def test_invalid_page(self):
        html = self.api.page(175451000)
        assert html is None
