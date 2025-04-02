import unittest

import requests_mock

from app import create_app


class GeneralWagtailTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("config.Test").test_client()
        self.domain = "http://localhost"
        self.mock_api_url = self.app.application.config.get("WAGTAIL_API_URL")

    def test_no_api_response(self):
        rv = self.app.get("/foobar/")
        self.assertEqual(rv.status_code, 502)
        self.assertIn(
            '<h1 class="tna-heading-xl">There is a problem with the service</h1>',
            rv.text,
        )

    @requests_mock.Mocker()
    def test_invalid_api_response(self, m):
        mock_endpoint = (
            f"{self.mock_api_url}/pages/find/?format=json&html_path=/foobar/"
        )
        mock_respsone = "not json"
        m.get(mock_endpoint, json=mock_respsone, status_code=200)
        rv = self.app.get("/foobar/")
        self.assertEqual(rv.status_code, 502)
        self.assertIn(
            '<h1 class="tna-heading-xl">There is a problem with the service</h1>',
            rv.text,
        )

    @requests_mock.Mocker()
    def test_password_protected_preview_page(self, m):
        mock_endpoint = f"{self.mock_api_url}/pages/1/?format=json"
        mock_respsone = {
            "id": 1,
            "meta": {"privacy": "password", "locked": True},
            "message": "Password required to view this resource.",
        }
        m.get(mock_endpoint, json=mock_respsone, status_code=200)
        rv = self.app.get("/preview/1/")
        self.assertEqual(rv.status_code, 200)
        self.assertIn(
            '<h1 class="tna-heading-xl">Password required</h1>',
            rv.text,
        )

    @requests_mock.Mocker()
    def test_published_preview_page(self, m):
        mock_alias_endpoint = f"{self.mock_api_url}/pages/1/?format=json"
        mock_alias_respsone = {
            "id": 518,
            "meta": {"url": "/foobar/"},
        }
        m.get(mock_alias_endpoint, json=mock_alias_respsone, status_code=200)
        rv = self.app.get("/preview/1/")
        self.assertEqual(rv.status_code, 302)
        self.assertEqual(rv.location, "/foobar/")

    @requests_mock.Mocker()
    def test_alias_page_redirect(self, m):
        mock_alias_endpoint = (
            f"{self.mock_api_url}/pages/find/?format=json&html_path=/foobar-alias/"
        )
        mock_alias_respsone = {
            "id": 518,
            "meta": {"alias_of": {"id": 2, "url": "/foobar/"}},
        }
        m.get(mock_alias_endpoint, json=mock_alias_respsone, status_code=200)
        rv = self.app.get("/foobar-alias/")
        self.assertEqual(rv.status_code, 302)
        self.assertEqual(rv.location, "/foobar/")

    @requests_mock.Mocker()
    def test_page_not_found(self, m):
        mock_content_endpoint = (
            f"{self.mock_api_url}/pages/find/?format=json&html_path=/foobar/"
        )
        mock_redirect_endpoint = (
            f"{self.mock_api_url}/redirects/find/?format=json&path=/foobar/"
        )
        mock_respsone = {"message": "not found"}
        m.get(mock_content_endpoint, json=mock_respsone, status_code=404)
        m.get(mock_redirect_endpoint, json=mock_respsone, status_code=404)
        rv = self.app.get("/foobar/")
        self.assertEqual(rv.status_code, 404)
        self.assertIn(
            '<h1 class="tna-heading-xl">Page not found</h1>',
            rv.text,
        )

    @requests_mock.Mocker()
    def test_permanent_external_redirect(self, m):
        mock_content_endpoint = (
            f"{self.mock_api_url}/pages/find/?format=json&html_path=/foobar/"
        )
        mock_content_respsone = {"message": "not found"}
        m.get(mock_content_endpoint, json=mock_content_respsone, status_code=404)
        mock_redirect_endpoint = (
            f"{self.mock_api_url}/redirects/find/?format=json&path=/foobar/"
        )
        mock_redirect_respsone = {
            "id": 1,
            "path": "/foobar",
            "is_permanent": True,
            "link": "https://gov.uk/",
        }
        m.get(mock_redirect_endpoint, json=mock_redirect_respsone, status_code=200)
        rv = self.app.get("/foobar/")
        self.assertEqual(rv.status_code, 301)
        self.assertEqual(rv.location, "https://gov.uk/")

    @requests_mock.Mocker()
    def test_temporary_external_redirect(self, m):
        mock_content_endpoint = (
            f"{self.mock_api_url}/pages/find/?format=json&html_path=/foobar/"
        )
        mock_content_respsone = {"message": "not found"}
        m.get(mock_content_endpoint, json=mock_content_respsone, status_code=404)
        mock_redirect_endpoint = (
            f"{self.mock_api_url}/redirects/find/?format=json&path=/foobar/"
        )
        mock_redirect_respsone = {
            "id": 1,
            "path": "/foobar",
            "is_permanent": False,
            "link": "https://gov.uk/",
        }
        m.get(mock_redirect_endpoint, json=mock_redirect_respsone, status_code=200)
        rv = self.app.get("/foobar/")
        self.assertEqual(rv.status_code, 302)
        self.assertEqual(rv.location, "https://gov.uk/")
