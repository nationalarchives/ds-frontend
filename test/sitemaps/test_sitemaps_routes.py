import unittest

import requests_mock

from app import create_app


class SitemapsBlueprintTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("config.Test")
        self.client = self.app.test_client()
        self.domain = "https://localhost"
        self.mock_api_url = self.app.config["WAGTAIL_API_URL"]

    @requests_mock.Mocker()
    def test_sitemap_index(self, m):
        mock_endpoint = (
            f"{self.mock_api_url}/pages/sitemap/?offset=0&limit=1&format=json"
        )
        mock_respsone = {
            "meta": {"total_count": 1337},
            "items": [],
        }
        m.get(mock_endpoint, json=mock_respsone)
        with self.client as c:
            rv = c.get("/sitemap.xml")
            self.assertIn(f"<loc>{self.domain}/sitemaps/sitemap_1.xml</loc>", rv.text)
            self.assertIn(f"<loc>{self.domain}/sitemaps/sitemap_2.xml</loc>", rv.text)
            self.assertIn(f"<loc>{self.domain}/sitemaps/sitemap_3.xml</loc>", rv.text)
            self.assertNotIn(
                f"<loc>{self.domain}/sitemaps/sitemap_4.xml</loc>", rv.text
            )

    @requests_mock.Mocker()
    def test_sitemap_pages(self, m):
        mock_endpoint = (
            f"{self.mock_api_url}/pages/sitemap/?format=json&offset=0&limit=500"
        )
        mock_respsone = {
            "meta": {"total_count": 250},
            "items": [
                {
                    "full_url": f"{self.domain}/",
                    "last_published_at": "2026-02-04T16:02:57.309445Z",
                },
                {
                    "full_url": f"{self.domain}/explore-the-collection/",
                    "last_published_at": "2025-07-29T11:55:39.069358Z",
                },
                {
                    "full_url": f"{self.domain}/explore-the-collection/explore-by-topic/",
                    "last_published_at": "2025-07-30T10:32:42.694208Z",
                },
            ],
        }
        m.get(mock_endpoint, json=mock_respsone)
        with self.client as c:
            rv = c.get("/sitemaps/sitemap_1.xml")
            self.assertEqual(rv.status_code, 200)
            self.assertIn(f"<loc>{self.domain}/</loc>", rv.text)
            self.assertIn(f"<loc>{self.domain}/explore-the-collection/</loc>", rv.text)
            self.assertIn(
                f"<loc>{self.domain}/explore-the-collection/explore-by-topic/</loc>",
                rv.text,
            )
            self.assertIn("<lastmod>2026-02-04</lastmod>", rv.text)
            self.assertIn("<lastmod>2025-07-29</lastmod>", rv.text)
            self.assertIn("<lastmod>2025-07-30</lastmod>", rv.text)
