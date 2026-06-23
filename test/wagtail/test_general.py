import unittest
from urllib.parse import quote

import requests_mock

from app import create_app


class GeneralWagtailTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("config.Test")
        self.client = self.app.test_client()
        self.domain = "http://localhost"
        self.mock_api_url = self.app.config["WAGTAIL_API_URL"]

    def test_no_api_response(self):
        with self.client as c:
            rv = c.get("/foobar/")
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
        with self.client as c:
            rv = c.get("/foobar/")
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
        with self.client as c:
            rv = c.get("/preview/1/")
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
        with self.client as c:
            rv = c.get("/preview/1/")
            self.assertEqual(rv.status_code, 302)
            self.assertEqual(rv.location, "/foobar/")

    @requests_mock.Mocker()
    def test_encoded_path_redirect(self, m):
        mock_alias_endpoint = (
            f"{self.mock_api_url}/pages/find/?format=json&html_path=/jam%C3%A9s-biggs/"
        )
        mock_alias_respsone = {
            "id": 518,
            "meta": {"url": "/jamés-biggs/"},
        }
        m.get(mock_alias_endpoint, json=mock_alias_respsone, status_code=200)
        with self.client as c:
            rv = c.get("/jam%C3%A9s-biggs/")
            self.assertEqual(rv.status_code, 302)
            self.assertEqual(rv.location, "/jam%C3%A9s-biggs/")
            rv = c.get("/jamés-biggs/")
            self.assertEqual(rv.status_code, 302)
            self.assertEqual(rv.location, "/jam%C3%A9s-biggs/")

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
        with self.client as c:
            rv = c.get("/foobar-alias/")
            self.assertEqual(rv.status_code, 302)
            self.assertEqual(rv.location, "/foobar/")

    @requests_mock.Mocker()
    def test_page_not_found_error(self, m):
        mock_content_endpoint = (
            f"{self.mock_api_url}/pages/find/?format=json&html_path=/foobar/"
        )
        mock_redirect_endpoint = (
            f"{self.mock_api_url}/redirects/find/?format=json&html_path=/foobar"
        )
        mock_respsone = {"message": "not found"}
        m.get(mock_content_endpoint, json=mock_respsone, status_code=404)
        m.get(mock_redirect_endpoint, json=mock_respsone, status_code=404)
        with self.client as c:
            rv = c.get("/foobar/")
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
            f"{self.mock_api_url}/redirects/find/?format=json&html_path=/foobar"
        )
        mock_redirect_respsone = {
            "id": 1,
            "meta": {
                "type": "wagtailredirects.Redirect",
                "detail_url": f"{self.mock_api_url}/redirects/1/",
            },
            "old_path": "/foobar",
            "location": "https://gov.uk/",
            "is_permanent": True,
        }
        m.get(mock_redirect_endpoint, json=mock_redirect_respsone, status_code=200)
        with self.client as c:
            rv = c.get("/foobar/")
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
            f"{self.mock_api_url}/redirects/find/?format=json&html_path=/foobar"
        )
        mock_redirect_respsone = {
            "id": 1,
            "meta": {
                "type": "wagtailredirects.Redirect",
                "detail_url": f"{self.mock_api_url}/redirects/1/",
            },
            "old_path": "/foobar",
            "location": "https://gov.uk/",
            "is_permanent": False,
        }
        m.get(mock_redirect_endpoint, json=mock_redirect_respsone, status_code=200)
        with self.client as c:
            rv = c.get("/foobar/")
            self.assertEqual(rv.status_code, 302)
            self.assertEqual(rv.location, "https://gov.uk/")

    @requests_mock.Mocker()
    def test_redirect_with_querystring(self, m):
        mock_content_endpoint = (
            f"{self.mock_api_url}/pages/find/?format=json&html_path=/foobar/"
        )
        mock_content_respsone = {"message": "not found"}
        m.get(mock_content_endpoint, json=mock_content_respsone, status_code=404)
        mock_redirect_endpoint = f"{self.mock_api_url}/redirects/find/?format=json&html_path={quote('/foobar?a=foo&b=bar')}"
        mock_redirect_respsone = {
            "id": 1,
            "meta": {
                "type": "wagtailredirects.Redirect",
                "detail_url": f"{self.mock_api_url}/redirects/1/",
            },
            "old_path": "/foobar?a=foo&b=bar",
            "location": "https://gov.uk/",
            "is_permanent": True,
        }
        m.get(mock_redirect_endpoint, json=mock_redirect_respsone, status_code=200)
        with self.client as c:
            rv = c.get("/foobar/?b=bar&a=foo")
            self.assertEqual(rv.status_code, 301)
            self.assertEqual(rv.location, "https://gov.uk/")

    @requests_mock.Mocker()
    def test_archived_page(self, m):
        m.get(
            f"{self.app.config['WAGTAIL_API_URL']}/pages/find/?format=json&html_path=%2F20s-people%2F&include_aliases=",
            status_code=404,
        )
        m.get(
            f"{self.app.config['WAGTAIL_API_URL']}/redirects/find/?format=json&html_path=%2F20s-people",
            status_code=404,
        )
        m.get(
            f"{self.app.config['WEBARCHIVE_CDXJ_API_URL']}/{self.app.config['WEBARCHIVE_CDXJ_API_PATH']}?url=https%3A%2F%2Fwww.nationalarchives.gov.uk%2F20s-people%2F&output=json&filter=status%3A200&limit=1&sort=reverse",
            json={
                "urlkey": "uk,gov,nationalarchives)/20s-people",
                "timestamp": "20260203071146",
                "url": "https://www.nationalarchives.gov.uk/20s-people/",
                "mime": "text/html",
                "status": "200",
                "digest": "GBB6XLMDQKSQCDF7BBWEPQW5AADHLVUQ",
                "redirect": "-",
                "robotflags": "-",
                "length": "13422",
                "offset": "343939131",
                "filename": "MW-TNAUKGWA-72364-000-20260203070431-www.nationalarchives.gov.uk-00123.warc.gz",
                "source": "full_zipnum",
                "source-coll": "full_zipnum",
                "access": "allow",
            },
        )
        with self.client as c:
            rv = c.get("/20s-people/", base_url="https://www.nationalarchives.gov.uk")
            self.assertEqual(rv.status_code, 410)
            self.assertIn("Page no longer exists", rv.text)
            self.assertIn("Error code: 410", rv.text)
            self.assertIn("Cache-Control", rv.headers)
            self.assertEqual(rv.headers["Cache-Control"], "no-store")
