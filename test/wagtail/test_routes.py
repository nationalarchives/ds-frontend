import unittest
from uuid import uuid4

import requests_mock

from app import create_app


class WagtailRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("config.Test")
        self.client = self.app.test_client()
        self.api = self.app.config["WAGTAIL_API_URL"]
        self.uuid = str(uuid4())

    def mock_webarchive(self, m, status_code=200):
        url = f"{self.app.config['WEBARCHIVE_CDXJ_API_URL']}/{self.app.config['WEBARCHIVE_CDXJ_API_PATH']}"
        m.get(url, json={}, status_code=status_code)

    def mock_page_not_found(self, m):
        m.get(f"{self.api}/pages/find/", json={"message": "not found"}, status_code=404)
        m.get(
            f"{self.api}/redirects/find/",
            json={"message": "not found"},
            status_code=404,
        )


class PageRouteTestCase(WagtailRoutesTestCase):
    @requests_mock.Mocker()
    def test_page_api_server_error(self, m):
        m.get(f"{self.api}/pages/find/", json={}, status_code=500)
        rv = self.client.get("/foobar/")
        self.assertEqual(rv.status_code, 502)

    @requests_mock.Mocker()
    def test_page_without_meta(self, m):
        m.get(f"{self.api}/pages/find/", json={"id": 1}, status_code=200)
        rv = self.client.get("/foobar/")
        self.assertEqual(rv.status_code, 502)

    @requests_mock.Mocker()
    def test_alias_redirect_disabled(self, m):
        self.app.config["REDIRECT_WAGTAIL_ALIAS_PAGES"] = False
        self.app.config["SERVE_WAGTAIL_PAGE_REDIRECTIONS"] = False
        m.get(
            f"{self.api}/pages/find/",
            json={"id": 1, "meta": {"alias_of": {"id": 2, "url": "/foobar/"}}},
            status_code=200,
        )
        rv = self.client.get("/foobar-alias/")
        self.assertNotEqual(rv.status_code, 302)

    @requests_mock.Mocker()
    def test_page_url_redirect_disabled(self, m):
        self.app.config["SERVE_WAGTAIL_PAGE_REDIRECTIONS"] = False
        m.get(
            f"{self.api}/pages/find/",
            json={"id": 1, "meta": {"url": "/other/"}},
            status_code=200,
        )
        rv = self.client.get("/foobar/")
        self.assertNotEqual(rv.status_code, 302)

    @requests_mock.Mocker()
    def test_page_url_redirect_to_canonical(self, m):
        m.get(
            f"{self.api}/pages/find/",
            json={"id": 1, "meta": {"url": "/other/"}},
            status_code=200,
        )
        rv = self.client.get("/foobar/")
        self.assertEqual(rv.status_code, 302)
        self.assertEqual(rv.location, "/other/")


class ExternalRedirectTestCase(WagtailRoutesTestCase):
    @requests_mock.Mocker()
    def test_external_redirects_disabled(self, m):
        self.app.config["SERVE_WAGTAIL_EXTERNAL_REDIRECTIONS"] = False
        m.get(f"{self.api}/pages/find/", json={}, status_code=404)
        m.get(
            f"{self.api}/redirects/find/",
            json={"location": "https://gov.uk/"},
            status_code=200,
        )
        self.mock_webarchive(m)
        rv = self.client.get("/foobar/")
        self.assertEqual(rv.status_code, 404)
        self.assertFalse(
            any("/redirects/find/" in r.url for r in m.request_history),
        )

    @requests_mock.Mocker()
    def test_redirect_api_server_error(self, m):
        m.get(f"{self.api}/pages/find/", json={}, status_code=404)
        m.get(f"{self.api}/redirects/find/", json={}, status_code=500)
        rv = self.client.get("/foobar/")
        self.assertEqual(rv.status_code, 502)

    @requests_mock.Mocker()
    def test_redirect_without_location_defaults_to_root(self, m):
        m.get(f"{self.api}/pages/find/", json={}, status_code=404)
        m.get(
            f"{self.api}/redirects/find/",
            json={"id": 1, "is_permanent": True},
            status_code=200,
        )
        rv = self.client.get("/foobar/")
        self.assertEqual(rv.status_code, 301)
        self.assertEqual(rv.location, "/")

    @requests_mock.Mocker()
    def test_redirect_query_string_is_sorted(self, m):
        m.get(f"{self.api}/pages/find/", json={}, status_code=404)
        m.get(
            f"{self.api}/redirects/find/",
            json={"location": "https://gov.uk/", "is_permanent": False},
            status_code=200,
        )
        rv = self.client.get("/foobar/?z=1&a=2&m=3")
        self.assertEqual(rv.status_code, 302)
        redirect_request = next(
            r for r in m.request_history if "/redirects/find/" in r.url
        )
        self.assertEqual(redirect_request.qs["html_path"], ["/foobar?a=2&m=3&z=1"])

    @requests_mock.Mocker()
    def test_not_found_when_webarchive_fails(self, m):
        self.mock_page_not_found(m)
        self.mock_webarchive(m, 500)
        rv = self.client.get("/foobar/")
        self.assertEqual(rv.status_code, 404)


class PreviewTestCase(WagtailRoutesTestCase):
    def test_preview_missing_parameters(self):
        for url in ("/preview/", "/preview/?token=abc", "/preview/?content_type=x"):
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 404)

    @requests_mock.Mocker()
    def test_preview_api_errors(self, m):
        self.mock_webarchive(m)
        for api_status, expected in ((404, 404), (403, 403), (500, 502)):
            with self.subTest(api_status=api_status):
                m.get(f"{self.api}/page_preview/1/", json={}, status_code=api_status)
                rv = self.client.get("/preview/?content_type=a.b&token=abc")
                self.assertEqual(rv.status_code, expected)

    @requests_mock.Mocker()
    def test_preview_render_failure(self, m):
        m.get(f"{self.api}/page_preview/1/", json={"id": 1}, status_code=200)
        rv = self.client.get("/preview/?content_type=a.b&token=abc")
        self.assertEqual(rv.status_code, 502)

    @requests_mock.Mocker()
    def test_protected_preview_api_errors(self, m):
        self.mock_webarchive(m)
        for api_status, expected in ((404, 404), (403, 403), (500, 502)):
            with self.subTest(api_status=api_status):
                m.get(f"{self.api}/pages/1/", json={}, status_code=api_status)
                rv = self.client.get("/preview/1/")
                self.assertEqual(rv.status_code, expected)

    @requests_mock.Mocker()
    def test_protected_preview_unprotected_page_without_url(self, m):
        m.get(f"{self.api}/pages/1/", json={"id": 1, "meta": {}}, status_code=200)
        rv = self.client.get("/preview/1/")
        self.assertEqual(rv.status_code, 502)


class PermalinkTestCase(WagtailRoutesTestCase):
    @requests_mock.Mocker()
    def test_permalink_redirects_to_page(self, m):
        m.get(
            f"{self.api}/pages/1/",
            json={"id": 1, "meta": {"url": "/foobar/"}},
            status_code=200,
        )
        rv = self.client.get("/page/1/")
        self.assertEqual(rv.status_code, 302)
        self.assertEqual(rv.location, "/foobar/")

    @requests_mock.Mocker()
    def test_permalink_without_url(self, m):
        m.get(f"{self.api}/pages/1/", json={"id": 1, "meta": {}}, status_code=200)
        rv = self.client.get("/page/1/")
        self.assertEqual(rv.status_code, 502)

    @requests_mock.Mocker()
    def test_permalink_api_errors(self, m):
        self.mock_webarchive(m)
        for api_status, expected in ((404, 404), (403, 403), (500, 502)):
            with self.subTest(api_status=api_status):
                m.get(f"{self.api}/pages/1/", json={}, status_code=api_status)
                rv = self.client.get("/page/1/")
                self.assertEqual(rv.status_code, expected)


class MediaTestCase(WagtailRoutesTestCase):
    @requests_mock.Mocker()
    def test_media_api_errors(self, m):
        self.mock_webarchive(m)
        for api_status, expected in ((404, 404), (403, 403), (500, 502)):
            with self.subTest(api_status=api_status):
                m.get(f"{self.api}/media/{self.uuid}/", json={}, status_code=api_status)
                rv = self.client.get(f"/video/{self.uuid}/")
                self.assertEqual(rv.status_code, expected)

    @requests_mock.Mocker()
    def test_media_type_mismatch_redirects(self, m):
        m.get(
            f"{self.api}/media/{self.uuid}/",
            json={"media_type": "audio"},
            status_code=200,
        )
        rv = self.client.get(f"/video/{self.uuid}/")
        self.assertEqual(rv.status_code, 302)
        self.assertEqual(rv.location, f"/audio/{self.uuid}/")

    @requests_mock.Mocker()
    def test_image_api_errors(self, m):
        self.mock_webarchive(m)
        for api_status, expected in ((404, 404), (403, 403), (500, 502)):
            with self.subTest(api_status=api_status):
                m.get(
                    f"{self.api}/images/{self.uuid}/", json={}, status_code=api_status
                )
                rv = self.client.get(f"/image/{self.uuid}/")
                self.assertEqual(rv.status_code, expected)


class ExploreTheCollectionSearchTestCase(WagtailRoutesTestCase):
    def test_invalid_page_number(self):
        for page in ("abc", "0", "-1"):
            with self.subTest(page=page):
                rv = self.client.get(f"/explore-the-collection/search/?page={page}")
                self.assertEqual(rv.status_code, 400)

    @requests_mock.Mocker()
    def test_page_beyond_last_page(self, m):
        self.mock_webarchive(m)
        m.get(
            f"{self.api}/pages/",
            json={"meta": {"total_count": 5}, "items": []},
            status_code=200,
        )
        rv = self.client.get("/explore-the-collection/search/?q=a&page=3")
        self.assertEqual(rv.status_code, 404)
