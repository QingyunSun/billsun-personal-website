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

    def test_agi_house_event_list_uses_button_link(self) -> None:
        self.assertIn('class="network-pill"', self.html)
        self.assertIn(">Event List</a>", self.html)

    def test_core_identity_copy_exists(self) -> None:
        self.assertIn("Bill Sun", self.html)
        self.assertIn("Qingyun Sun", self.html)
        self.assertIn("AI researcher", self.html)
        self.assertIn("Stanford", self.html)
        self.assertIn("Early transformer", self.html)
        self.assertIn("the first researcher at Google Brain", self.html)

    def test_research_roots_copy_exists(self) -> None:
        self.assertIn("the mathematics of AI", self.html)
        self.assertIn("the first researcher at Google Brain to make", self.html)
        self.assertIn("the Transformer work on QA (2016)", self.html)
        self.assertIn("Published at ICML, NeurIPS, AAAI, CVPR, and CoRL", self.html)

    def test_research_roots_card_is_shortened(self) -> None:
        self.assertIn("Stanford Math PhD focused on the mathematical structure of AI", self.html)
        self.assertIn("new model architectures.", self.html)
        self.assertNotIn("During his PhD, he used", self.html)

    def test_about_section_lists_three_big_problems(self) -> None:
        self.assertIn("From AI structure to financial intelligence.", self.html)
        self.assertIn("Three problems I keep returning to.", self.html)
        self.assertIn("Recursive self-improvement", self.html)
        self.assertIn("Continual learning", self.html)
        self.assertIn("Multimodal pretraining", self.html)
        self.assertIn("microstructure", self.html)
        self.assertIn('class="problem-grid"', self.html)

    def test_multi_agents_card_copy_exists(self) -> None:
        self.assertIn("Multi-agents", self.html)
        self.assertIn("Protocol and new market design", self.html)
        self.assertIn("smart contracts, poker, trading.", self.html)

    def test_research_and_timeline_copy_is_sharper(self) -> None:
        self.assertIn("Five themes that shape the work.", self.html)
        self.assertIn("Early transformer work at Google Brain", self.html)
        self.assertIn("RL, stochastic control, portfolio optimization", self.html)
        self.assertIn("Main arcs, reduced to essentials.", self.html)
        self.assertIn("Built an AI-powered forecast trading team", self.html)

    def test_network_copy_is_tightened(self) -> None:
        self.assertIn("Hosted and guest conversations across AI, crypto, robotics,", self.html)
        self.assertIn("Bay Area AI builder network linking", self.html)
        self.assertIn("community co-organized with Tim Shi", self.html)

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
        cls.ids = parser.ids
        cls.links = parser.links
        cls.images = parser.images

    def test_podcast_page_does_not_use_placeholder_covers(self) -> None:
        self.assertNotIn(
            "../assets/podcast/generated/podcast-placeholder.svg",
            self.images,
        )

    def test_podcast_page_uses_language_sections(self) -> None:
        self.assertTrue({"english", "chinese"}.issubset(self.ids))
        self.assertTrue({"overview", "hosted", "guest", "archive"}.isdisjoint(self.ids))

    def test_more_sections_exist_and_default_closed(self) -> None:
        self.assertIn('id="more-english"', self.html)
        self.assertIn('id="more-chinese"', self.html)
        self.assertNotIn('id="more-english" class="podcast-more" open', self.html)
        self.assertNotIn('id="more-chinese" class="podcast-more" open', self.html)
        self.assertIn("Top 9", self.html)
        self.assertIn("Top 3", self.html)

    def test_new_podcast_covers_are_referenced(self) -> None:
        expected_images = {
            "../assets/podcast/stripe-on-stable-coin.png",
            "../assets/podcast/talk-to-announce-aiusd.png",
            "../assets/podcast/building-ai-trader.png",
            "../assets/podcast/sophia-interview-on-anthropic.png",
            "../assets/podcast/bedrock-ai-investing.jpg",
            "../assets/podcast/haseeb-dragonfly.jpg",
            "../assets/podcast/primora-interview.jpg",
            "../assets/podcast/video/cttv-apec-gen-alpha-agent.png",
            "../assets/podcast/youtube/wxPs6j35_oQ.jpg",
            "../assets/podcast/youtube/njZ3oYLsRck.jpg",
            "../assets/podcast/youtube/oVMC9T7KzQE.jpg",
            "../assets/podcast/youtube/JLWGJ6NC6X8.jpg",
            "../assets/podcast/youtube/BV1bWrPYMEjM.jpg",
            "../assets/podcast/youtube/BV1tCHQzhEjB.jpg",
        }
        self.assertTrue(expected_images.issubset(set(self.images)))

    def test_new_bilibili_links_are_present(self) -> None:
        expected_links = {
            "https://www.bilibili.com/video/BV1bWrPYMEjM/",
            "https://www.bilibili.com/video/BV1tCHQzhEjB/",
        }
        self.assertTrue(expected_links.issubset(set(self.links)))

    def test_haseeb_link_is_split_from_semianalysis(self) -> None:
        haseeb_link = "https://x.com/BillSun_AI/status/1985943572504592759?s=20"
        self.assertEqual(self.html.count(haseeb_link), 1)
        self.assertIn("Haseeb, Managing Partner at Dragonfly", self.html)
        self.assertNotIn("X Post 2", self.html)

    def test_jie_tan_uses_youtube_link(self) -> None:
        self.assertIn("https://www.youtube.com/watch?v=NLLmIIfcZZM", self.html)
        self.assertNotIn("https://x.com/BillSun_AI/status/1981487539929436606?s=20", self.html)
        self.assertNotIn("https://x.com/i/broadcasts/1YqJDNbNRjQKV", self.html)

    def test_cttv_clip_is_listed_in_more_chinese(self) -> None:
        self.assertIn("CCTV 财经采访：APEC 期间报道硅谷 AI Agent 创业公司", self.html)
        self.assertIn("https://x.com/BillSun_AI/status/2043213031820439619?s=20", self.links)
        self.assertNotIn("../assets/podcast/video/cttv-apec-gen-alpha-agent.mp4", self.links)
        self.assertIn("2023 年中文电视采访", self.html)

    def test_bedrock_card_prefers_youtube_before_wechat(self) -> None:
        card = self.html.split("<h3>Bedrock 聊聊AI在投资的应用</h3>", 1)[1].split("</article>", 1)[0]
        youtube = "https://www.youtube.com/watch?v=5gp3g_pMyTU"
        wechat = "https://mp.weixin.qq.com/s/ZmQHy_YbNaC2BTVrLnYOpQ"
        self.assertIn(youtube, card)
        self.assertIn(wechat, card)
        self.assertLess(card.index(youtube), card.index(wechat))

    def test_bilingual_bilibili_episode_is_grouped_under_chinese(self) -> None:
        title = "[英语播客]从对冲基金到AGI：斯坦福博士Bill Sun的双重人生"
        english_section = self.html.split('<section id="english"', 1)[1].split('<section id="chinese"', 1)[0]
        chinese_section = self.html.split('<section id="chinese"', 1)[1]
        self.assertNotIn(title, english_section)
        self.assertIn(title, chinese_section)

    def test_featured_english_expands_to_top_nine(self) -> None:
        english_section = self.html.split('<section id="english"', 1)[1].split('<details id="more-english"', 1)[0]
        for title in {
            "Illia Polosukhin (Transformer paper authors)",
            "Building AI Trader with Reasoning and RAG | Bill Sun | Generative Alpha | RetrieveX 2024",
            "Revolutionizing Financial Research, AI-Powered Investment Analysis | Grace Gong",
        }:
            self.assertIn(title, english_section)
        self.assertNotIn("<h3>NEAR</h3>", english_section)

    def test_tim_shi_card_prefers_youtube_before_x_post(self) -> None:
        card = self.html.split("<h3>Tim Shi, Alex Chen and Monica Xie</h3>", 1)[1].split("</article>", 1)[0]
        youtube = "https://www.youtube.com/watch?v=FEu3oT5r6lc"
        x_post = "https://x.com/BillSun_AI/status/1859814533948493930"
        self.assertIn(youtube, card)
        self.assertIn(x_post, card)
        self.assertLess(card.index(youtube), card.index(x_post))


if __name__ == "__main__":
    unittest.main()
