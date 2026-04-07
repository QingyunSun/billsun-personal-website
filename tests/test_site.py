import html.parser
import pathlib
import unittest


SITE_ROOT = pathlib.Path(__file__).resolve().parents[1]
INDEX_PATH = SITE_ROOT / "index.html"
PODCAST_PATH = SITE_ROOT / "podcast" / "index.html"


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
            "/podcast/",
            "https://stanford.edu/~qysun/",
            "https://www.linkedin.com/in/qingyun-sun",
            "https://scholar.google.com/citations?user=POXzrBYAAAAJ&hl=en",
            "https://x.com/BillSun_AI",
            "https://www.youtube.com/@Billsun_ai",
            "https://www.agihouse.org/",
            "https://agihouse-app.web.app/events",
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

    def test_podcast_page_exists(self) -> None:
        self.assertTrue(PODCAST_PATH.exists())


class PodcastPageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.html = PODCAST_PATH.read_text(encoding="utf-8")
        parser = SiteParser()
        parser.feed(cls.html)
        cls.images = parser.images

    def test_podcast_page_does_not_use_placeholder_covers(self) -> None:
        self.assertNotIn(
            "../assets/podcast/generated/podcast-placeholder.svg",
            self.images,
        )

    def test_new_podcast_covers_are_referenced(self) -> None:
        expected_images = {
            "../assets/podcast/stripe-on-stable-coin.png",
            "../assets/podcast/talk-to-announce-aiusd.png",
            "../assets/podcast/building-ai-trader.png",
            "../assets/podcast/sophia-interview-on-anthropic.png",
        }
        self.assertTrue(expected_images.issubset(set(self.images)))


if __name__ == "__main__":
    unittest.main()
