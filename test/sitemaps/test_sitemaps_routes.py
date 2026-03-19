import unittest

import requests_mock

from app import create_app


class SitemapsBlueprintTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("config.Test").test_client()
        self.domain = "http://localhost"
        self.mock_api_url = self.app.application.config["WAGTAIL_API_URL"]

    @requests_mock.Mocker()
    def test_sitemap_index(self, m):
        domain = self.domain.replace("http://", "https://")
        mock_endpoint = f"{self.mock_api_url}/pages/?offset=0&limit=1&format=json"
        mock_respsone = {
            "meta": {"total_count": 1337},
            "items": [],
        }
        m.get(mock_endpoint, json=mock_respsone)
        rv = self.app.get("/sitemap.xml")
        self.assertIn(f"<loc>{domain}/sitemaps/sitemap_1.xml</loc>", rv.text)
        self.assertIn(f"<loc>{domain}/sitemaps/sitemap_2.xml</loc>", rv.text)
        self.assertIn(f"<loc>{domain}/sitemaps/sitemap_3.xml</loc>", rv.text)
        self.assertNotIn(f"<loc>{domain}/sitemaps/sitemap_4.xml</loc>", rv.text)

    @requests_mock.Mocker()
    def test_sitemap_page_1_xml(self, m):
        domain = self.domain.replace("http://", "https://")
        mock_index_endpoint = f"{self.mock_api_url}/pages/?offset=0&limit=1&format=json"
        mock_index_respsone = {
            "meta": {"total_count": 250},
            "items": [],
        }
        m.get(mock_index_endpoint, json=mock_index_respsone)
        mock_endpoint = f"{self.mock_api_url}/pages/?offset=0&limit=500&format=json"
        mock_respsone = {
            "meta": {"total_count": 3},
            "items": [
                {
                    "id": 3,
                    "title": "The National Archives Beta",
                    "short_title": "The National Archives Beta",
                    "page_path": "/",
                    "url": f"{domain}/",
                    "full_url": f"{domain}/",
                    "type": "home.HomePage",
                    "type_label": "Home",
                    "teaser_text": "ETNA homepage",
                    "teaser_image": None,
                    "first_published_at": "2021-07-28T09:37:55.003000Z",
                    "last_published_at": "2026-02-04T16:02:57.309445Z",
                },
                {
                    "id": 5,
                    "title": "Explore the collection",
                    "short_title": "Explore the collection",
                    "page_path": "/explore-the-collection/",
                    "url": f"{domain}/explore-the-collection/",
                    "full_url": f"{domain}/explore-the-collection/",
                    "type": "collections.ExplorerIndexPage",
                    "type_label": "Explorer index",
                    "teaser_text": "Choose a topic or time period and start exploring some of our most important and unusual records.",
                    "teaser_image": {
                        "id": 1305,
                        "title": "Large collection of letters sent on the Spanish ship La Perla",
                        "jpeg": {
                            "url": "/media/images/prize-p.2e16d0ba.fill-600x400.format-jpeg.jpegquality-60_W4BMfq1.jpg",
                            "full_url": f"{domain}/media/images/prize-p.2e16d0ba.fill-600x400.format-jpeg.jpegquality-60_W4BMfq1.jpg",
                            "width": 600,
                            "height": 400,
                        },
                        "webp": {
                            "url": "/media/images/prize-.2e16d0ba.fill-600x400.format-webp.webpquality-80_bk8AKep.webp",
                            "full_url": f"{domain}/media/images/prize-.2e16d0ba.fill-600x400.format-webp.webpquality-80_bk8AKep.webp",
                            "width": 600,
                            "height": 400,
                        },
                    },
                    "first_published_at": "2021-04-15T15:37:56.896513Z",
                    "last_published_at": "2025-07-29T11:55:39.069358Z",
                },
                {
                    "id": 53,
                    "title": "Explore by topic",
                    "short_title": "Explore by topic",
                    "page_path": "/explore-the-collection/explore-by-topic/",
                    "url": f"{domain}/explore-the-collection/explore-by-topic/",
                    "full_url": f"{domain}/explore-the-collection/explore-by-topic/",
                    "type": "collections.TopicExplorerIndexPage",
                    "type_label": "Topic explorer index",
                    "teaser_text": "Our collection shines a light on many aspects of life, from the stories of states to different people's experiences. Browse these topics for just a taste.",
                    "teaser_image": {
                        "id": 1352,
                        "title": "Map of Chertsey Abbey teaser",
                        "jpeg": {
                            "url": "/media/images/map-of-.2e16d0ba.fill-600x400.format-jpeg.jpegquality-60_Mh4oeUt.jpg",
                            "full_url": f"{domain}/media/images/map-of-.2e16d0ba.fill-600x400.format-jpeg.jpegquality-60_Mh4oeUt.jpg",
                            "width": 600,
                            "height": 400,
                        },
                        "webp": {
                            "url": "/media/images/map-of.2e16d0ba.fill-600x400.format-webp.webpquality-80_e9FuoI4.webp",
                            "full_url": f"{domain}/media/images/map-of.2e16d0ba.fill-600x400.format-webp.webpquality-80_e9FuoI4.webp",
                            "width": 600,
                            "height": 400,
                        },
                    },
                    "first_published_at": "2021-07-13T13:05:42.402902Z",
                    "last_published_at": "2025-07-30T10:32:42.694208Z",
                },
            ],
        }
        m.get(mock_endpoint, json=mock_respsone)
        rv = self.app.get("/sitemaps/sitemap_1.xml")
        self.assertEqual(rv.status_code, 200)
        self.assertIn(f"<loc>{domain}/</loc>", rv.text)
        self.assertIn(f"<loc>{domain}/explore-the-collection/</loc>", rv.text)
        self.assertIn(
            f"<loc>{domain}/explore-the-collection/explore-by-topic/</loc>",
            rv.text,
        )
        self.assertIn("<lastmod>2026-02-04</lastmod>", rv.text)
        self.assertIn("<lastmod>2025-07-29</lastmod>", rv.text)
        self.assertIn("<lastmod>2025-07-30</lastmod>", rv.text)
