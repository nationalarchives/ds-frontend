import unittest

from flask import Flask, Response

from app.lib.content_negotiation import get_requested_accept


class RequestedAcceptTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)

    def test_negotiated_type_is_passed_by_keyword(self):
        @get_requested_accept(["text/html", "text/markdown"])
        def page(path, *, preferred_content_type):
            return f"{path}: {preferred_content_type}"

        cases = (
            ({}, None),
            ({"Accept": ""}, None),
            ({"Accept": " , , "}, None),
            ({"Accept": "text/markdown"}, "text/markdown"),
            ({"Accept": "TEXT/MARKDOWN"}, "text/markdown"),
            ({"Accept": "text/html;q=0.5, text/markdown;q=0.9"}, "text/markdown"),
            ({"Accept": "text/markdown;q=0.3, text/html;q=0.8"}, "text/html"),
            ({"Accept": "*/*"}, "text/html"),
            ({"Accept": "text/*"}, "text/html"),
            ({"Accept": "text/markdown, text/html"}, "text/html"),
            ({"Accept": "text/markdown;q=0.5, text/html;q=0.5"}, "text/html"),
            ({"Accept": "*/*;q=1, text/html;q=0.1"}, "text/markdown"),
            ({"Accept": "text/html;q=0.1, */*;q=1"}, "text/markdown"),
            ({"Accept": "*/*, text/html;q=0"}, "text/markdown"),
            ({"Accept": "text/html;q=0, */*"}, "text/markdown"),
            ({"Accept": "text/*;q=0, */*"}, None),
            ({"Accept": "text/*;q=0, text/html;q=0.5"}, "text/html"),
            ({"Accept": "application/json"}, None),
            ({"Accept": "image/*"}, None),
            ({"Accept": "*/*;q=0"}, None),
            ({"Accept": "text/html;q=0, text/markdown;q=0"}, None),
        )
        for headers, expected in cases:
            with (
                self.subTest(headers=headers),
                self.app.test_request_context(headers=headers),
            ):
                for args, kwargs in (
                    (("/example/",), {}),
                    ((), {"path": "/example/"}),
                ):
                    response = page(*args, **kwargs)
                    self.assertEqual(
                        response.get_data(as_text=True), f"/example/: {expected}"
                    )
                    self.assertIn("Accept", response.vary)

        self.assertEqual(page.__name__, "page")

    def test_invalid_quality_entries_are_ignored(self):
        @get_requested_accept(["text/html", "text/markdown"])
        def page(*, preferred_content_type):
            return str(preferred_content_type)

        for quality in ("invalid", "2", "-1", "NaN", "inf"):
            with (
                self.subTest(quality=quality),
                self.app.test_request_context(
                    headers={"Accept": f"text/html;q={quality}, text/markdown;q=0.5"}
                ),
            ):
                response = page()
                self.assertEqual(response.get_data(as_text=True), "text/markdown")

    def test_equal_matches_use_supported_type_order(self):
        @get_requested_accept(["text/markdown", "text/html"])
        def page(*, preferred_content_type):
            return preferred_content_type

        for header in ("*/*", "text/*", "text/html, text/markdown"):
            with (
                self.subTest(header=header),
                self.app.test_request_context(headers={"Accept": header}),
            ):
                self.assertEqual(page().get_data(as_text=True), "text/markdown")

    def test_preserves_response_status_body_and_custom_headers(self):
        original_response = Response("page content", status=201)
        original_response.headers["X-Example"] = "preserved"

        @get_requested_accept(["text/html"])
        def page(*, preferred_content_type):
            return original_response

        with self.app.test_request_context():
            response = page()

        self.assertIs(response, original_response)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_data(as_text=True), "page content")
        self.assertEqual(response.headers["X-Example"], "preserved")
        self.assertIn("Accept", response.vary)

    def test_preserves_tuple_response_status_and_headers(self):
        @get_requested_accept(["text/html"])
        def page(*, preferred_content_type):
            return "page content", 202, {"X-Example": "preserved"}

        with self.app.test_request_context():
            response = page()

        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.get_data(as_text=True), "page content")
        self.assertEqual(response.headers["X-Example"], "preserved")
        self.assertIn("Accept", response.vary)

    def test_preserves_existing_vary_values_without_duplicate_accept(self):
        for vary in ("Accept-Encoding", "Accept-Encoding, Accept"):
            with self.subTest(vary=vary):
                original_response = Response("page content", headers={"Vary": vary})

                @get_requested_accept(["text/html"])
                def page(*, preferred_content_type, response=original_response):
                    return response

                with self.app.test_request_context():
                    response = page()

                self.assertEqual(set(response.vary), {"Accept-Encoding", "Accept"})
                self.assertEqual(
                    [value.lower() for value in response.vary].count("accept"), 1
                )

    def test_empty_supported_types_passes_none(self):
        @get_requested_accept([])
        def page(*, preferred_content_type):
            self.assertIsNone(preferred_content_type)
            return "page content"

        with self.app.test_request_context(headers={"Accept": "text/html"}):
            response = page()

        self.assertEqual(response.get_data(as_text=True), "page content")
        self.assertIn("Accept", response.vary)

    def test_preserves_function_metadata(self):
        def page(*, preferred_content_type):
            """Render a page."""
            return "page content"

        decorated = get_requested_accept(["text/html"])(page)

        self.assertEqual(decorated.__name__, page.__name__)
        self.assertEqual(decorated.__doc__, page.__doc__)
        self.assertIs(decorated.__wrapped__, page)
