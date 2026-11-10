import unittest
from unittest.mock import patch
from uuid import uuid4

import requests_mock
from flask import Response

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
    def test_cookies_page_disallows_markdown(self):
        html = "<main><p>Cookie preferences</p></main>"
        cases = (
            ({}, 200),
            ({"Accept": "text/html"}, 200),
            ({"Accept": "text/markdown, text/html;q=0.5"}, 200),
            ({"Accept": "text/markdown, text/*;q=0.5"}, 200),
            ({"Accept": "text/markdown, */*;q=0.5"}, 200),
            ({"Accept": "text/markdown"}, 406),
            ({"Accept": "text/markdown, text/html;q=0"}, 406),
            ({"Accept": "*/*, text/html;q=0"}, 406),
            ({"Accept": "application/json"}, 406),
        )
        for headers, status in cases:
            with (
                self.subTest(headers=headers),
                patch(
                    "app.wagtail.routes.page_details_by_uri",
                    return_value={
                        "id": 1,
                        "meta": {"url": "/cookies/", "type": "cookies.CookiesPage"},
                    },
                ),
                patch(
                    "app.wagtail.pages.cookies.cookies_page.page_children",
                    return_value={"items": [{"id": 2}]},
                ) as children,
                patch(
                    "app.wagtail.pages.cookies.cookies_page.render_template",
                    return_value=html,
                ) as render,
            ):
                response = self.client.get("/cookies/", headers=headers)
                self.assertEqual(response.status_code, status)
                self.assertEqual(response.mimetype, "text/html")
                self.assertIn("Accept", response.vary)
                if status == 200:
                    self.assertEqual(response.get_data(as_text=True), html)
                    self.assertIn("Cookie", response.vary)
                    children.assert_called_once()
                    render.assert_called_once()
                else:
                    self.assertEqual(response.headers["Cache-Control"], "no-store")
                    children.assert_not_called()
                    render.assert_not_called()

        with (
            patch(
                "app.wagtail.routes.page_details_by_uri",
                return_value={"id": 3, "meta": {"url": "/other/"}},
            ),
            patch("app.wagtail.routes.render_content_page", return_value=html),
        ):
            response = self.client.get("/other/", headers={"Accept": "text/markdown"})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.mimetype, "text/markdown")
            self.assertEqual(response.get_data(as_text=True), "Cookie preferences")

    def test_registered_page_negotiates_accept(self):
        html = "<nav>Navigation</nav><main><p>rendered page</p></main>"
        cases = (
            ({}, "text/html", html),
            ({"Accept": "text/html"}, "text/html", html),
            ({"Accept": "*/*"}, "text/html", html),
            ({"Accept": "application/json"}, "text/html", html),
            ({"Accept": "text/markdown, text/html"}, "text/html", html),
            (
                {"Accept": "text/html;q=invalid, text/markdown;q=0.5"},
                "text/markdown",
                "rendered page",
            ),
            (
                {"Accept": "text/html;q=0, text/markdown;q=0"},
                "text/html",
                html,
            ),
            ({"Accept": "text/markdown"}, "text/markdown", "rendered page"),
            (
                {"Accept": "text/html;q=0.5, text/markdown;q=0.9"},
                "text/markdown",
                "rendered page",
            ),
        )
        for path in ("/", "/foobar/"):
            for headers, mimetype, body in cases:
                with (
                    self.subTest(path=path, headers=headers),
                    patch(
                        "app.wagtail.routes.page_details_by_uri",
                        return_value={"id": 1, "meta": {"url": path}},
                    ),
                    patch(
                        "app.wagtail.routes.render_content_page",
                        return_value=Response(html, mimetype="text/html"),
                    ),
                ):
                    response = self.client.get(path, headers=headers)
                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(response.mimetype, mimetype)
                    self.assertEqual(response.get_data(as_text=True), body)
                    self.assertIn("Accept", response.vary)

    def test_markdown_conversion_handles_strings_and_responses(self):
        html = (
            "<html><body><nav>Navigation</nav><main>"
            "<p><strong>Caf\u00e9</strong> and "
            '<a href="https://example.com/">a link</a>.</p>'
            "</main><footer>Footer</footer></body></html>"
        )
        for as_response in (False, True):
            with (
                self.subTest(as_response=as_response),
                patch(
                    "app.wagtail.routes.page_details_by_uri",
                    return_value={"id": 1, "meta": {"url": "/foobar/"}},
                ),
                patch(
                    "app.wagtail.routes.render_content_page",
                    return_value=(
                        Response(html, mimetype="text/html") if as_response else html
                    ),
                ),
            ):
                response = self.client.get(
                    "/foobar/", headers={"Accept": "text/markdown"}
                )
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.mimetype, "text/markdown")
                self.assertEqual(
                    response.get_data(as_text=True),
                    "**Caf\u00e9** and [a link](https://example.com/).",
                )
                self.assertEqual(response.content_length, len(response.data))
                self.assertIn("Accept", response.vary)

    def test_markdown_preserves_status_and_headers(self):
        original_response = Response(
            "<main><p>Content</p></main>",
            status=203,
            mimetype="text/html",
            headers={
                "Cache-Control": "public, max-age=300",
                "Vary": "Accept-Encoding",
                "X-Example": "preserved",
            },
        )
        original_response.set_cookie("first", "one")
        original_response.set_cookie("second", "two")
        with (
            patch(
                "app.wagtail.routes.page_details_by_uri",
                return_value={"id": 1, "meta": {"url": "/foobar/"}},
            ),
            patch(
                "app.wagtail.routes.render_content_page", return_value=original_response
            ),
        ):
            response = self.client.get("/foobar/", headers={"Accept": "text/markdown"})

        self.assertEqual(response.status_code, 203)
        self.assertEqual(response.get_data(as_text=True), "Content")
        self.assertEqual(response.content_type, "text/markdown; charset=utf-8")
        self.assertEqual(response.content_length, len(b"Content"))
        self.assertEqual(response.headers["Cache-Control"], "public, max-age=300")
        self.assertEqual(response.headers["X-Example"], "preserved")
        self.assertEqual(
            response.headers.getlist("Set-Cookie"),
            ["first=one; Path=/", "second=two; Path=/"],
        )
        self.assertEqual(set(response.vary), {"Accept-Encoding", "Accept"})

    def test_markdown_removes_original_body_validators_and_digests(self):
        body_headers = {
            "ETag": '"html-version"',
            "Content-MD5": "html-checksum",
            "Digest": "sha-256=html-checksum",
            "Content-Digest": "sha-256=:html-checksum:",
            "Repr-Digest": "sha-256=:html-checksum:",
        }
        for accept in ("text/html", "text/markdown"):
            with (
                self.subTest(accept=accept),
                patch(
                    "app.wagtail.routes.page_details_by_uri",
                    return_value={"id": 1, "meta": {"url": "/foobar/"}},
                ),
                patch(
                    "app.wagtail.routes.render_content_page",
                    return_value=Response(
                        "<main><p>Content</p></main>",
                        mimetype="text/html",
                        headers=body_headers,
                    ),
                ),
            ):
                response = self.client.get("/foobar/", headers={"Accept": accept})
                self.assertEqual(response.status_code, 200)
                for header, value in body_headers.items():
                    if accept == "text/html":
                        self.assertEqual(response.headers[header], value)
                    else:
                        self.assertNotIn(header, response.headers)

    def test_markdown_does_not_convert_rendered_errors_or_redirects(self):
        html = "<main><p>Original response</p></main>"
        for status in (302, 400, 403, 404, 500, 502):
            for as_tuple in (False, True):
                headers = {
                    "Cache-Control": "no-store",
                    "Content-Type": "text/html; charset=utf-8",
                    "ETag": '"original"',
                    "Vary": "Accept-Encoding",
                }
                if status == 302:
                    headers["Location"] = "/other/"
                rendered = (
                    (html, status, headers)
                    if as_tuple
                    else Response(html, status=status, headers=headers)
                )
                with (
                    self.subTest(status=status, as_tuple=as_tuple),
                    patch(
                        "app.wagtail.routes.page_details_by_uri",
                        return_value={"id": 1, "meta": {"url": "/foobar/"}},
                    ),
                    patch(
                        "app.wagtail.routes.render_content_page",
                        return_value=rendered,
                    ),
                ):
                    response = self.client.get(
                        "/foobar/", headers={"Accept": "text/markdown"}
                    )
                    self.assertEqual(response.status_code, status)
                    self.assertEqual(response.get_data(as_text=True), html)
                    self.assertEqual(response.mimetype, "text/html")
                    self.assertEqual(response.headers["Cache-Control"], "no-store")
                    self.assertEqual(response.headers["ETag"], '"original"')
                    self.assertEqual(set(response.vary), {"Accept-Encoding", "Accept"})
                    if status == 302:
                        self.assertEqual(response.location, "/other/")

    @requests_mock.Mocker()
    def test_markdown_preserves_real_renderer_errors(self, m):
        self.mock_webarchive(m)
        for page_type, expected in ((None, 502), ("unknown.Page", 404)):
            with self.subTest(page_type=page_type):
                m.get(
                    f"{self.api}/pages/find/",
                    json={
                        "id": 1,
                        "meta": {"url": "/foobar/", "type": page_type},
                    },
                )
                response = self.client.get(
                    "/foobar/", headers={"Accept": "text/markdown"}
                )
                self.assertEqual(response.status_code, expected)
                self.assertEqual(response.mimetype, "text/html")
                self.assertIn(b"<", response.data)
                self.assertIn("Accept", response.vary)

    def test_markdown_without_main_converts_whole_document(self):
        cases = (
            (
                "<nav>Navigation</nav><p>Content</p><footer>Footer</footer>",
                "Navigation\n\nContent\n\nFooter",
            ),
            ("<nav>Navigation</nav><main></main><footer>Footer</footer>", ""),
            ("", ""),
        )
        for html, expected in cases:
            with (
                self.subTest(html=html),
                patch(
                    "app.wagtail.routes.page_details_by_uri",
                    return_value={"id": 1, "meta": {"url": "/foobar/"}},
                ),
                patch("app.wagtail.routes.render_content_page", return_value=html),
            ):
                response = self.client.get(
                    "/foobar/", headers={"Accept": "text/markdown"}
                )
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.mimetype, "text/markdown")
                self.assertEqual(response.get_data(as_text=True), expected)
                self.assertEqual(response.content_length, len(response.data))

    @requests_mock.Mocker()
    def test_markdown_request_preserves_redirect(self, m):
        m.get(
            f"{self.api}/pages/find/",
            json={"id": 1, "meta": {"url": "/other/"}},
        )
        response = self.client.get("/foobar/", headers={"Accept": "text/markdown"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, "/other/")
        self.assertEqual(response.mimetype, "text/html")
        self.assertIn("Accept", response.vary)

    @requests_mock.Mocker()
    def test_markdown_request_preserves_errors(self, m):
        self.app.config["SERVE_WAGTAIL_EXTERNAL_REDIRECTIONS"] = False
        self.mock_webarchive(m)
        for api_status, expected in ((404, 404), (500, 502)):
            with self.subTest(api_status=api_status):
                m.get(f"{self.api}/pages/find/", json={}, status_code=api_status)
                response = self.client.get(
                    "/foobar/", headers={"Accept": "text/markdown"}
                )
                self.assertEqual(response.status_code, expected)
                self.assertEqual(response.mimetype, "text/html")
                self.assertTrue(response.data)
                self.assertIn("Accept", response.vary)

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
        self.assertEqual(rv.headers["Cache-Control"], "no-store")


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
