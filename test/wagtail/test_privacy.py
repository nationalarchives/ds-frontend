import unittest

from aioresponses import aioresponses

from app import create_app


class WagtailPrivacyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("config.Test")
        self.client = self.app.test_client()
        self.domain = "http://localhost"
        self.mock_api_url = self.app.config["WAGTAIL_API_URL"]

    def test_private_page_preview_redirection(self):
        with aioresponses() as m:
            mock_endpoint = (
                f"{self.mock_api_url}/pages/find/"
                "?format=json&html_path=/foobar/&include_aliases="
            )
            mock_respsone = {
                "id": 352,
                "meta": {"privacy": "password", "locked": True},
                "message": "Password required to view this resource.",
            }
            m.get(mock_endpoint, payload=mock_respsone)
            rv = self.client.get("/foobar/")
            self.assertEqual(rv.status_code, 302)
            self.assertEqual(rv.location, "/preview/352/")

    def test_private_page_password_page(self):
        with aioresponses() as m:
            mock_endpoint = (
                f"{self.mock_api_url}/pages/352/"
                "?format=json&password=&include_aliases="
            )
            mock_respsone = {
                "id": 352,
                "meta": {"privacy": "password", "locked": True},
                "message": "Password required to view this resource.",
            }
            m.get(mock_endpoint, payload=mock_respsone)
            rv = self.client.get("/preview/352/")
            self.assertEqual(rv.status_code, 200)
            self.assertIn(
                '<h1 class="tna-heading-xl">Password required</h1>',
                rv.text,
            )
            self.assertIn(
                "Enter the password",
                rv.text,
            )

    def test_private_page_password_page_post_blank_password(self):
        with aioresponses() as m:
            mock_endpoint = (
                f"{self.mock_api_url}/pages/352/"
                "?format=json&password=&include_aliases="
            )
            mock_respsone = {
                "id": 352,
                "meta": {"privacy": "password", "locked": True},
                "message": "Password required to view this resource.",
            }
            m.get(mock_endpoint, payload=mock_respsone)
            rv = self.client.post(
                "/preview/352/",
                content_type="multipart/form-data",
                data={"password": ""},
            )
            self.assertEqual(rv.status_code, 200)
            self.assertIn(
                '<h1 class="tna-heading-xl">Password required</h1>',
                rv.text,
            )
            self.assertIn(
                "There is a problem",
                rv.text,
            )
            self.assertIn(
                '<span class="tna-!--visually-hidden">Error:</span> Enter a password',
                rv.text,
            )

    def test_private_page_password_page_post_wrong_password(self):
        with aioresponses() as m:
            mock_endpoint = (
                f"{self.mock_api_url}/pages/352/"
                "?format=json&password=wrongpassword&include_aliases="
            )
            mock_respsone = {
                "id": 352,
                "meta": {"privacy": "password", "locked": True},
                "message": "Incorrect password.",
            }
            m.get(mock_endpoint, payload=mock_respsone)
            rv = self.client.post(
                "/preview/352/",
                content_type="multipart/form-data",
                data={"password": "wrongpassword"},
            )
            self.assertEqual(rv.status_code, 200)
            self.assertIn(
                '<h1 class="tna-heading-xl">Password required</h1>',
                rv.text,
            )
            self.assertIn(
                "There is a problem",
                rv.text,
            )
            self.assertIn(
                '<span class="tna-!--visually-hidden">Error:</span> Incorrect password',
                rv.text,
            )

    def test_private_page_password_page_post_correct_password(self):
        with aioresponses() as m:
            mock_endpoint = (
                f"{self.mock_api_url}/pages/352/"
                "?format=json&password=correctpassword&include_aliases="
            )
            mock_respsone = {
                "id": 352,
                "meta": {"type": "articles.ArticlePage", "privacy": "password"},
                "topics": [],
                "time_periods": [],
            }
            m.get(mock_endpoint, payload=mock_respsone)
            rv = self.client.post(
                "/preview/352/",
                content_type="multipart/form-data",
                data={"password": "correctpassword"},
            )
            self.assertEqual(rv.status_code, 200)
            self.assertNotIn(
                '<h1 class="tna-heading-xl">Password required</h1>',
                rv.text,
            )
            self.assertNotIn(
                "There is a problem",
                rv.text,
            )
            self.assertNotIn(
                '<span class="tna-!--visually-hidden">Error:</span> Enter a password',
                rv.text,
            )
            self.assertNotIn(
                '<span class="tna-!--visually-hidden">Error:</span> Incorrect password',
                rv.text,
            )

    def test_private_page_redirect_for_non_private_pages(self):
        with aioresponses() as m:
            mock_endpoint = (
                f"{self.mock_api_url}/pages/352/"
                "?format=json&password=&include_aliases="
            )
            mock_respsone = {
                "id": 352,
                "meta": {
                    "type": "articles.ArticlePage",
                    "privacy": "public",
                    "url": "/foobar/",
                },
            }
            m.get(mock_endpoint, payload=mock_respsone)
            rv = self.client.get("/preview/352/")
            self.assertEqual(rv.status_code, 302)
            self.assertEqual(rv.location, "/foobar/")
