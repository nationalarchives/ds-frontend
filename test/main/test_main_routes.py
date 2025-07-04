import unittest

from app import create_app


class MainBlueprintTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("config.Test").test_client()
        self.domain = "http://localhost"
        self.mock_api_url = self.app.application.config.get("WAGTAIL_API_URL")

    def test_trailing_slash_redirects(self):
        rv = self.app.get("/healthcheck/live")
        self.assertEqual(rv.status_code, 308)
        self.assertEqual(rv.location, f"{self.domain}/healthcheck/live/")

    def test_trailing_slash_redirects_with_querystrings(self):
        rv = self.app.get("/healthcheck/live?foo=bar")
        self.assertEqual(rv.status_code, 308)
        self.assertEqual(rv.location, f"{self.domain}/healthcheck/live/?foo=bar")

    def test_healthcheck_live(self):
        rv = self.app.get("/healthcheck/live/")
        self.assertEqual(rv.status_code, 200)
        self.assertIn("ok", rv.text)
