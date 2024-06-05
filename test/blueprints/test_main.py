import unittest

import requests
import requests_mock

from app import create_app


class MainBlueprintTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("config.Test").test_client()

    def test_healthcheck_live(self):
        rv = self.app.get("/healthcheck/live/")
        self.assertEqual(rv.status_code, 200)
        self.assertIn("ok", rv.text)

    def test_browse(self):
        rv = self.app.get("/browse/")
        self.assertEqual(rv.status_code, 200)
        self.assertIn("Explore 1,000 years of history", rv.text)

    def test_sitemap_xml(self):
        with requests_mock.Mocker() as m:
            mock_api_url = self.app.application.config["WAGTAIL_API_URL"]
            mock_endpoint = (
                f"{mock_api_url}/pages/?offset=0&limit=20&format=json"
            )
            mock_respsone = {
                "meta": {"total_count": 2},
                "items": [
                    {
                        "id": 3,
                        "title": "The National Archives Beta",
                        "url": "/",
                        "full_url": f"{self.app.application.config["DOMAIN"]}/",
                        "type_label": "Home",
                        "teaser_text": "ETNA homepage",
                        "teaser_image": None,
                    },
                    {
                        "id": 5,
                        "title": "Explore the collection",
                        "url": "/explore-the-collection/",
                        "full_url": f"{self.app.application.config["DOMAIN"]}/explore-the-collection/",
                        "type_label": "Explorer index",
                        "teaser_text": "Choose a topic or time period and start exploring some of our most important and unusual records.",
                        "teaser_image": {
                            "id": 1305,
                            "title": "Large collection of letters sent on the Spanish ship La Perla",
                            "jpeg": {
                                "url": "/media/images/prize-p.2e16d0ba.fill-600x400.format-jpeg.jpegquality-60_W4BMfq1.jpg",
                                "full_url": f"{self.app.application.config["MEDIA_DOMAIN"]}/media/images/prize-p.2e16d0ba.fill-600x400.format-jpeg.jpegquality-60_W4BMfq1.jpg",
                                "width": 600,
                                "height": 400,
                            },
                            "webp": {
                                "url": "/media/images/prize-.2e16d0ba.fill-600x400.format-webp.webpquality-80_bk8AKep.webp",
                                "full_url": f"{self.app.application.config["MEDIA_DOMAIN"]}/media/images/prize-.2e16d0ba.fill-600x400.format-webp.webpquality-80_bk8AKep.webp",
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
            self.assertIn(f"<loc>{self.app.application.config["DOMAIN"]}/</loc>", rv.text)
            self.assertIn(
                f"<loc>{self.app.application.config["DOMAIN"]}/explore-the-collection/</loc>", rv.text
            )
            self.assertIn(f"<loc>{self.app.application.config["DOMAIN"]}/browse/</loc>", rv.text)
            self.assertIn(f"<loc>{self.app.application.config["DOMAIN"]}/legal/</loc>", rv.text)
            self.assertIn(f"<loc>{self.app.application.config["DOMAIN"]}/legal/cookies/</loc>", rv.text)
            self.assertIn(
                f"<loc>{self.app.application.config["DOMAIN"]}/legal/cookie-details/</loc>", rv.text
            )

    def test_404(self):
        rv = self.app.get("/foobar/")
        self.assertEqual(rv.status_code, 404)
