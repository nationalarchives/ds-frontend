import unittest

from app import create_app


class MainBlueprintTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("config.Test")
        self.client = self.app.test_client()
        self.domain = "http://localhost"
        self.mock_api_url = self.app.config["WAGTAIL_API_URL"]

    def test_trailing_slash_redirects(self):
        rv = self.client.get("/healthcheck/live")
        self.assertEqual(rv.status_code, 308)
        self.assertEqual(rv.location, f"{self.domain}/healthcheck/live/")

    def test_trailing_slash_redirects_with_querystrings(self):
        rv = self.client.get("/healthcheck/live?foo=bar")
        self.assertEqual(rv.status_code, 308)
        self.assertEqual(rv.location, f"{self.domain}/healthcheck/live/?foo=bar")

    def test_healthcheck_live(self):
        rv = self.client.get("/healthcheck/live/")
        self.assertEqual(rv.status_code, 200)
        self.assertIn("ok", rv.text)
        self.assertIn("Cache-Control", rv.headers)
        self.assertEqual(rv.headers["Cache-Control"], "no-store")

    def test_healthcheck_version(self):
        rv = self.client.get("/healthcheck/version/")
        self.assertEqual(rv.status_code, 200)
        self.assertIn(self.app.config["BUILD_VERSION"], rv.text)
        self.assertIn("Cache-Control", rv.headers)
        self.assertEqual(rv.headers["Cache-Control"], "no-store")

    def test_well_known_security(self):
        rv = self.client.get("/.well-known/security.txt")
        self.assertEqual(rv.status_code, 200)
        self.assertIn("Contact: ", rv.text)
        self.assertIn("Preferred-Languages: ", rv.text)
        self.assertIn("Canonical: ", rv.text)
        self.assertIn("Policy: ", rv.text)
        self.assertIn("Expires: ", rv.text)
        self.assertIn("Cache-Control", rv.headers)
        self.assertEqual(rv.headers["Cache-Control"], "no-cache")

    def test_well_known_disclosure_policy(self):
        rv = self.client.get("/.well-known/disclosure-policy.txt")
        self.assertEqual(rv.status_code, 200)
        self.assertIn("Cache-Control", rv.headers)
        self.assertEqual(rv.headers["Cache-Control"], "no-cache")

    def test_well_known_thanks(self):
        rv = self.client.get("/.well-known/thanks.txt")
        self.assertEqual(rv.status_code, 200)
        self.assertIn("Cache-Control", rv.headers)
        self.assertEqual(rv.headers["Cache-Control"], "no-cache")

    def test_well_known_risky_paths(self):
        rv = self.client.get("/.well-known/./security.txt")
        self.assertEqual(rv.status_code, 200)
        self.assertIn("Contact: ", rv.text)
        self.assertIn("Cache-Control", rv.headers)
        self.assertEqual(rv.headers["Cache-Control"], "no-cache")

        rv = self.client.get("/.well-known/~/security.txt")
        self.assertEqual(rv.status_code, 404)
        self.assertIn("Cache-Control", rv.headers)
        self.assertEqual(rv.headers["Cache-Control"], "no-store")

        rv = self.client.get("/.well-known/../security.txt")
        self.assertEqual(rv.status_code, 404)
        self.assertIn("Cache-Control", rv.headers)
        self.assertEqual(rv.headers["Cache-Control"], "no-store")

        rv = self.client.get("/.well-known/~/.bashrc")
        self.assertEqual(rv.status_code, 404)
        self.assertIn("Cache-Control", rv.headers)
        self.assertEqual(rv.headers["Cache-Control"], "no-store")

        rv = self.client.get("/.well-known//security.txt")
        self.assertEqual(rv.status_code, 308)
        self.assertEqual(rv.location, "http://localhost/.well-known//security.txt/")

    def test_robots(self):
        rv = self.client.get("/robots.txt")
        self.assertEqual(rv.status_code, 200)
        self.assertIn("Cache-Control", rv.headers)
        self.assertEqual(rv.headers["Cache-Control"], "public, max-age=14400")

    def test_manifest(self):
        rv = self.client.get("/manifest.json")
        self.assertEqual(rv.status_code, 200)
        self.assertIn("Cache-Control", rv.headers)
        self.assertEqual(rv.headers["Cache-Control"], "public, max-age=14400")

    def test_set_cookies(self):
        rv = self.client.post(
            "/cookies/set/",
            data={"usage": "true", "settings": "true", "marketing": "false"},
        )
        self.assertEqual(rv.status_code, 302)
        self.assertIn("Set-Cookie", rv.headers)
        self.assertIn(
            "cookies_policy=%7B%22usage%22%3Atrue%2C%22settings%22%3Atrue%2C%22marketing%22%3Afalse%2C%22essential%22%3Atrue%7D",
            rv.headers["Set-Cookie"],
        )

    def test_set_cookies_inc_essential(self):
        rv = self.client.post(
            "/cookies/set/",
            data={
                "usage": "true",
                "settings": "true",
                "marketing": "true",
                "essential": "false",
            },
        )
        self.assertEqual(rv.status_code, 302)
        self.assertIn("Set-Cookie", rv.headers)
        self.assertIn(
            "cookies_policy=%7B%22usage%22%3Atrue%2C%22settings%22%3Atrue%2C%22marketing%22%3Atrue%2C%22essential%22%3Atrue%7D",
            rv.headers["Set-Cookie"],
        )

    def test_set_cookies_partial(self):
        rv = self.client.post(
            "/cookies/set/",
            data={"usage": "true"},
        )
        self.assertEqual(rv.status_code, 302)
        self.assertIn("Set-Cookie", rv.headers)
        self.assertIn(
            "cookies_policy=%7B%22usage%22%3Atrue%2C%22settings%22%3Afalse%2C%22marketing%22%3Afalse%2C%22essential%22%3Atrue%7D",
            rv.headers["Set-Cookie"],
        )

    def test_set_cookies_incorrect(self):
        rv = self.client.post(
            "/cookies/set/",
            data={"foo": "bar", "usage": "pizza"},
        )
        self.assertEqual(rv.status_code, 302)
        self.assertIn("Set-Cookie", rv.headers)
        self.assertIn(
            "cookies_policy=%7B%22usage%22%3Afalse%2C%22settings%22%3Afalse%2C%22marketing%22%3Afalse%2C%22essential%22%3Atrue%7D",
            rv.headers["Set-Cookie"],
        )

    def test_set_cookies_invalid(self):
        rv = self.client.post(
            "/cookies/set/",
            data="foobar",
        )
        self.assertEqual(rv.status_code, 302)
        self.assertIn("Set-Cookie", rv.headers)
        self.assertIn(
            "cookies_policy=%7B%22usage%22%3Afalse%2C%22settings%22%3Afalse%2C%22marketing%22%3Afalse%2C%22essential%22%3Atrue%7D",
            rv.headers["Set-Cookie"],
        )

    def test_set_cookies_really_bad(self):
        rv = self.client.post(
            "/cookies/set/",
            data={"settings": "&quot; xssattr_marker=&quot;"},
        )
        self.assertEqual(rv.status_code, 302)
        self.assertIn("Set-Cookie", rv.headers)
        self.assertIn(
            "cookies_policy=%7B%22usage%22%3Afalse%2C%22settings%22%3Afalse%2C%22marketing%22%3Afalse%2C%22essential%22%3Atrue%7D",
            rv.headers["Set-Cookie"],
        )
