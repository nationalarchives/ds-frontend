import unittest

from app import create_app


class MainBlueprintTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("config.Test")
        self.client = self.app.test_client()

    def test_400(self):
        rv = self.client.get("/400/")
        self.assertEqual(rv.status_code, 400)
        self.assertIn("The page you requested cannot be served", rv.text)
        self.assertIn("Cache-Control", rv.headers)
        self.assertEqual(rv.headers["Cache-Control"], "no-store")

    def test_403(self):
        rv = self.client.get("/403/")
        self.assertEqual(rv.status_code, 403)
        self.assertIn("Restricted", rv.text)
        self.assertIn("Cache-Control", rv.headers)
        self.assertEqual(rv.headers["Cache-Control"], "no-store")

    def test_404(self):
        rv = self.client.get("/404/")
        self.assertEqual(rv.status_code, 404)
        self.assertIn("Page not found", rv.text)
        self.assertIn("Cache-Control", rv.headers)
        self.assertEqual(rv.headers["Cache-Control"], "no-store")

    def test_500(self):
        rv = self.client.get("/500/")
        self.assertEqual(rv.status_code, 500)
        self.assertIn("There is a problem with the service", rv.text)
        self.assertIn("Cache-Control", rv.headers)
        self.assertEqual(rv.headers["Cache-Control"], "no-store")

    def test_502(self):
        rv = self.client.get("/502/")
        self.assertEqual(rv.status_code, 502)
        self.assertIn("There is a problem with the service", rv.text)
        self.assertIn("Cache-Control", rv.headers)
        self.assertEqual(rv.headers["Cache-Control"], "no-store")
