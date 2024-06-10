import json
import unittest

import requests_mock

from app import create_app


class WagtailPrivacyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("config.Test").test_client()
        self.domain = self.app.application.config["DOMAIN"]
        self.media_domain = self.app.application.config["MEDIA_DOMAIN"]
        self.mock_api_url = self.app.application.config["WAGTAIL_API_URL"]

    @requests_mock.Mocker()
    def test_private_page_preview_redirection(self, m):
        mock_endpoint = (
            f"{self.mock_api_url}/pages/find/?html_path=foobar&format=json"
        )
        mock_respsone = {
            "id": 352,
            "meta": {"privacy": "password", "locked": True},
            "message": "Password required to view this resource.",
        }
        m.get(mock_endpoint, json=mock_respsone)
        rv = self.app.get("/foobar/")
        self.assertEqual(rv.status_code, 302)
        self.assertEqual(rv.location, "/preview/352/")

    @requests_mock.Mocker()
    def test_private_page_password_page(self, m):
        mock_endpoint = f"{self.mock_api_url}/pages/352/?format=json"
        mock_respsone = {
            "id": 352,
            "meta": {"privacy": "password", "locked": True},
            "message": "Password required to view this resource.",
        }
        m.get(mock_endpoint, json=mock_respsone)
        rv = self.app.get("/preview/352/")
        self.assertEqual(rv.status_code, 200)
        self.assertIn(
            '<h1 class="tna-heading-xl">Password required</h1>',
            rv.text,
        )
        self.assertIn(
            "Enter the password",
            rv.text,
        )

    @requests_mock.Mocker()
    def test_private_page_password_page_post_blank_password(self, m):
        mock_endpoint = f"{self.mock_api_url}/pages/352/?password=&format=json"
        mock_respsone = {
            "id": 352,
            "meta": {"privacy": "password", "locked": True},
            "message": "Password required to view this resource.",
        }
        m.get(mock_endpoint, json=mock_respsone)
        rv = self.app.post(
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

    @requests_mock.Mocker()
    def test_private_page_password_page_post_wrong_password(self, m):
        mock_endpoint = (
            f"{self.mock_api_url}/pages/352/?password=wrongpassword&format=json"
        )
        mock_respsone = {
            "id": 352,
            "meta": {"privacy": "password", "locked": True},
            "message": "Incorrect password.",
        }
        m.get(mock_endpoint, json=mock_respsone)
        rv = self.app.post(
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

    @requests_mock.Mocker()
    def test_private_page_password_page_post_correct_password(self, m):
        mock_endpoint = f"{self.mock_api_url}/pages/352/?password=correctpassword&format=json"
        mock_respsone = {
            "id": 352,
            "meta": {"type": "articles.ArticlePage", "privacy": "password"},
            "topics": [],
            "time_periods": [],
        }
        m.get(mock_endpoint, json=mock_respsone)
        rv = self.app.post(
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

    @requests_mock.Mocker()
    def test_private_page_redirect_for_non_private_pages(self, m):
        mock_endpoint = f"{self.mock_api_url}/pages/352/?password=&format=json"
        mock_respsone = {
            "id": 352,
            "meta": {
                "type": "articles.ArticlePage",
                "privacy": "public",
                "url": "/foobar/",
            },
        }
        m.get(mock_endpoint, json=mock_respsone)
        rv = self.app.get("/preview/352/")
        self.assertEqual(rv.status_code, 302)
        self.assertEqual(rv.location, "/foobar/")
