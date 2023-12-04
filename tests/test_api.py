from src.api import WikiData, WikiPedia


class TestWikiData:
    api = WikiData()

    def test_entity(self):
        content = self.api.entity(15920546)
        assert "Q15920546" in content["entities"]

    def test_invalid_entity(self):
        content = self.api.entity(159205460)
        assert "missing" in content["entities"]["Q159205460"]


class TestWikiPedia:
    api = WikiPedia()

    def test_page(self):
        content = self.api.page(17545100)
        html = content["parse"]["text"]["*"]
        assert isinstance(html, str)

    def test_invalid_page(self):
        content = self.api.page(175451000)
        assert "error" in content
