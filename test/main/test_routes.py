import unittest

import requests_mock

from app import create_app


class MainBlueprintTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("config.Test").test_client()
        self.domain = "http://localhost"
        self.mock_api_url = self.app.application.config["WAGTAIL_API_URL"]

    def test_trailing_slash_redirects(self):
        rv = self.app.get("/healthcheck/live")
        self.assertEqual(rv.status_code, 308)
        self.assertEqual(rv.location, f"{self.domain}/healthcheck/live/")

    def test_healthcheck_live(self):
        rv = self.app.get("/healthcheck/live/")
        self.assertEqual(rv.status_code, 200)
        self.assertIn("ok", rv.text)

    def test_browse(self):
        rv = self.app.get("/browse/")
        self.assertEqual(rv.status_code, 200)
        self.assertIn("Explore 1,000 years of history", rv.text)

    @requests_mock.Mocker()
    def test_sitemap_xml(self, m):
        mock_endpoint = (
            f"{self.mock_api_url}/pages/?offset=0&limit=20&format=json"
        )
        mock_respsone = {
            "meta": {"total_count": 3},
            "items": [
                {
                    "id": 3,
                    "title": "The National Archives Beta",
                    "url": "/",
                    "full_url": f"{self.domain}/",
                    "type_label": "Home",
                    "teaser_text": "ETNA homepage",
                    "teaser_image": None,
                },
                {
                    "id": 5,
                    "title": "Explore the collection",
                    "url": "/explore-the-collection/",
                    "full_url": f"{self.domain}/explore-the-collection/",
                    "type_label": "Explorer index",
                    "teaser_text": "Choose a topic or time period and start exploring some of our most important and unusual records.",
                    "teaser_image": {
                        "id": 1305,
                        "title": "Large collection of letters sent on the Spanish ship La Perla",
                        "jpeg": {
                            "url": "/media/images/prize-p.2e16d0ba.fill-600x400.format-jpeg.jpegquality-60_W4BMfq1.jpg",
                            "full_url": f"{self.domain}/media/images/prize-p.2e16d0ba.fill-600x400.format-jpeg.jpegquality-60_W4BMfq1.jpg",
                            "width": 600,
                            "height": 400,
                        },
                        "webp": {
                            "url": "/media/images/prize-.2e16d0ba.fill-600x400.format-webp.webpquality-80_bk8AKep.webp",
                            "full_url": f"{self.domain}/media/images/prize-.2e16d0ba.fill-600x400.format-webp.webpquality-80_bk8AKep.webp",
                            "width": 600,
                            "height": 400,
                        },
                    },
                },
                {
                    "id": 53,
                    "title": "Explore by topic",
                    "url": "/explore-the-collection/explore-by-topic/",
                    "full_url": f"{self.domain}/explore-the-collection/explore-by-topic/",
                    "type_label": "Topic explorer index",
                    "teaser_text": "Our collection shines a light on many aspects of life, from the stories of states to different people's experiences. Browse these topics for just a taste.",
                    "teaser_image": {
                        "id": 1352,
                        "title": "Map of Chertsey Abbey teaser",
                        "jpeg": {
                            "url": "/media/images/map-of-.2e16d0ba.fill-600x400.format-jpeg.jpegquality-60_Mh4oeUt.jpg",
                            "full_url": f"{self.domain}/media/images/map-of-.2e16d0ba.fill-600x400.format-jpeg.jpegquality-60_Mh4oeUt.jpg",
                            "width": 600,
                            "height": 400,
                        },
                        "webp": {
                            "url": "/media/images/map-of.2e16d0ba.fill-600x400.format-webp.webpquality-80_e9FuoI4.webp",
                            "full_url": f"{self.domain}/media/images/map-of.2e16d0ba.fill-600x400.format-webp.webpquality-80_e9FuoI4.webp",
                            "width": 600,
                            "height": 400,
                        },
                    },
                },
            ],
        }
        m.get(mock_endpoint, json=mock_respsone)
        rv = self.app.get("/sitemap.xml")
        self.assertEqual(rv.status_code, 200)
        self.assertIn(f"<loc>{self.domain}/</loc>", rv.text)
        self.assertIn(
            f"<loc>{self.domain}/explore-the-collection/</loc>", rv.text
        )
        self.assertIn(
            f"<loc>{self.domain}/explore-the-collection/explore-by-topic/</loc>",
            rv.text,
        )
        self.assertIn(f"<loc>{self.domain}/browse/</loc>", rv.text)
        self.assertIn(f"<loc>{self.domain}/legal/</loc>", rv.text)
        self.assertIn(f"<loc>{self.domain}/legal/cookies/</loc>", rv.text)
        self.assertIn(
            f"<loc>{self.domain}/legal/cookie-details/</loc>", rv.text
        )
