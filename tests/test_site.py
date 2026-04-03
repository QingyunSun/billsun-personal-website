import html.parser
import pathlib
import unittest


SITE_ROOT = pathlib.Path(__file__).resolve().parents[1]
INDEX_PATH = SITE_ROOT / "index.html"


class SiteParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.links: list[str] = []
        self.images: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = dict(attrs)
        if "id" in attr_map and attr_map["id"]:
            self.ids.add(attr_map["id"])
        if tag == "a" and attr_map.get("href"):
            self.links.append(attr_map["href"])
        if tag == "img" and attr_map.get("src"):
            self.images.append(attr_map["src"])


class SiteStructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.html = INDEX_PATH.read_text(encoding="utf-8")
        parser = SiteParser()
        parser.feed(cls.html)
        cls.ids = parser.ids
        cls.links = parser.links
        cls.images = parser.images

    def test_expected_sections_exist(self) -> None:
        expected = {"about", "timeline", "research", "network", "links"}
        self.assertTrue(expected.issubset(self.ids))

    def test_core_external_links_exist(self) -> None:
        expected_links = {
            "https://stanford.edu/~qysun/",
            "https://www.linkedin.com/in/qingyun-sun",
            "https://scholar.google.com/citations?user=POXzrBYAAAAJ&hl=en",
            "https://x.com/BillSun_AI",
            "https://www.youtube.com/@Billsun_ai",
        }
        self.assertTrue(expected_links.issubset(set(self.links)))

    def test_core_identity_copy_exists(self) -> None:
        self.assertIn("Bill Sun", self.html)
        self.assertIn("Qingyun Sun", self.html)
        self.assertIn("AI researcher", self.html)
        self.assertIn("Stanford", self.html)
        self.assertIn(
            "1st researcher in Google Brain to discover that Transformer works",
            self.html,
        )

    def test_portrait_asset_is_referenced(self) -> None:
        self.assertIn("./assets/qingyun-sun-portrait-1280.jpg", self.images)


if __name__ == "__main__":
    unittest.main()
