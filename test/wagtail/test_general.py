import unittest

from aioresponses import aioresponses

from app import create_app


class GeneralWagtailTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("config.Test")
        self.client = self.app.test_client()
        self.domain = "http://localhost"
        self.mock_api_url = self.app.config["WAGTAIL_API_URL"]

    def test_no_api_response(self):
        rv = self.client.get("/foobar/")
        self.assertEqual(rv.status_code, 502)
        self.assertIn(
            '<h1 class="tna-heading-xl">There is a problem with the service</h1>',
            rv.text,
        )

    def test_invalid_api_response(self):
        with aioresponses() as m:
            mock_endpoint = (
                f"{self.mock_api_url}/pages/find/"
                "?format=json&html_path=/foobar/&include_aliases="
            )
            mock_respsone = "not json"
            m.get(mock_endpoint, payload=mock_respsone)
            rv = self.client.get("/foobar/")
            self.assertEqual(rv.status_code, 502)
            self.assertIn(
                '<h1 class="tna-heading-xl">There is a problem with the service</h1>',
                rv.text,
            )

    def test_password_protected_preview_page(self):
        with aioresponses() as m:
            mock_endpoint = (
                f"{self.mock_api_url}/pages/1/"
                "?format=json&password=&include_aliases="
            )
            mock_respsone = {
                "id": 1,
                "meta": {"privacy": "password", "locked": True},
                "message": "Password required to view this resource.",
            }
            m.get(mock_endpoint, payload=mock_respsone)
            rv = self.client.get("/preview/1/")
            self.assertEqual(rv.status_code, 200)
            self.assertIn(
                '<h1 class="tna-heading-xl">Password required</h1>',
                rv.text,
            )

    def test_published_preview_page(self):
        with aioresponses() as m:
            mock_alias_endpoint = (
                f"{self.mock_api_url}/pages/1/"
                "?format=json&password=&include_aliases="
            )
            mock_alias_respsone = {
                "id": 518,
                "meta": {"url": "/foobar/"},
            }
            m.get(mock_alias_endpoint, payload=mock_alias_respsone)
            rv = self.client.get("/preview/1/")
            self.assertEqual(rv.status_code, 302)
            self.assertEqual(rv.location, "/foobar/")

    def test_encoded_path_redirect(self):
        with aioresponses() as m:
            mock_alias_endpoint = (
                f"{self.mock_api_url}/pages/find/"
                "?format=json&html_path=/jam%C3%A9s-biggs/&include_aliases="
            )
            mock_alias_respsone = {
                "id": 518,
                "meta": {"url": "/jamés-biggs/"},
            }
            m.get(mock_alias_endpoint, payload=mock_alias_respsone, repeat=True)
            rv = self.client.get("/jam%C3%A9s-biggs/")
            self.assertEqual(rv.status_code, 302)
            self.assertEqual(rv.location, "/jam%C3%A9s-biggs/")
            rv = self.client.get("/jamés-biggs/")
            self.assertEqual(rv.status_code, 302)
            self.assertEqual(rv.location, "/jam%C3%A9s-biggs/")

    def test_alias_page_redirect(self):
        with aioresponses() as m:
            mock_alias_endpoint = (
                f"{self.mock_api_url}/pages/find/"
                "?format=json&html_path=/foobar-alias/&include_aliases="
            )
            mock_alias_respsone = {
                "id": 518,
                "meta": {"alias_of": {"id": 2, "url": "/foobar/"}},
            }
            m.get(mock_alias_endpoint, payload=mock_alias_respsone)
            rv = self.client.get("/foobar-alias/")
            self.assertEqual(rv.status_code, 302)
            self.assertEqual(rv.location, "/foobar/")

    def test_page_not_found(self):
        with aioresponses() as m:
            mock_content_endpoint = (
                f"{self.mock_api_url}/pages/find/"
                "?format=json&html_path=/foobar/&include_aliases="
            )
            mock_redirect_endpoint = (
                f"{self.mock_api_url}/redirects/find/" "?format=json&html_path=/foobar"
            )
            mock_respsone = {"message": "not found"}
            m.get(mock_content_endpoint, payload=mock_respsone, status=404)
            m.get(mock_redirect_endpoint, payload=mock_respsone, status=404)
            rv = self.client.get("/foobar/")
            self.assertEqual(rv.status_code, 404)
            self.assertIn(
                '<h1 class="tna-heading-xl">Page not found</h1>',
                rv.text,
            )

    def test_permanent_external_redirect(self):
        with aioresponses() as m:
            mock_content_endpoint = (
                f"{self.mock_api_url}/pages/find/"
                "?format=json&html_path=/foobar/&include_aliases="
            )
            mock_content_respsone = {"message": "not found"}
            m.get(mock_content_endpoint, payload=mock_content_respsone, status=404)
            mock_redirect_endpoint = (
                f"{self.mock_api_url}/redirects/find/" "?format=json&html_path=/foobar"
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
            m.get(mock_redirect_endpoint, payload=mock_redirect_respsone)
            rv = self.client.get("/foobar/")
            self.assertEqual(rv.status_code, 301)
            self.assertEqual(rv.location, "https://gov.uk/")

    def test_temporary_external_redirect(self):
        with aioresponses() as m:
            mock_content_endpoint = (
                f"{self.mock_api_url}/pages/find/"
                "?format=json&html_path=/foobar/&include_aliases="
            )
            mock_content_respsone = {"message": "not found"}
            m.get(mock_content_endpoint, payload=mock_content_respsone, status=404)
            mock_redirect_endpoint = (
                f"{self.mock_api_url}/redirects/find/" "?format=json&html_path=/foobar"
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
            m.get(mock_redirect_endpoint, payload=mock_redirect_respsone)
            rv = self.client.get("/foobar/")
            self.assertEqual(rv.status_code, 302)
            self.assertEqual(rv.location, "https://gov.uk/")

    def test_redirect_with_querystring(self):
        with aioresponses() as m:
            mock_content_endpoint = (
                f"{self.mock_api_url}/pages/find/"
                "?format=json&html_path=/foobar/&include_aliases="
            )
            mock_content_respsone = {"message": "not found"}
            m.get(mock_content_endpoint, payload=mock_content_respsone, status=404)
            mock_redirect_endpoint = (
                f"{self.mock_api_url}/redirects/find/"
                "?format=json&html_path=/foobar?a%3Dfoo%26b%3Dbar"
            )
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
            m.get(mock_redirect_endpoint, payload=mock_redirect_respsone)
            rv = self.client.get("/foobar/?b=bar&a=foo")
            self.assertEqual(rv.status_code, 301)
            self.assertEqual(rv.location, "https://gov.uk/")
