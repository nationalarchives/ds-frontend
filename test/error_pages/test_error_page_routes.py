import unittest

from app import create_app


class ErrorPagesBlueprintTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("config.Test")
        self.client = self.app.test_client()

    def test_400(self):
        with self.client as c:
            rv = c.get("/error/400/")
            self.assertEqual(rv.status_code, 400)
            self.assertIn("The page you requested cannot be served", rv.text)
            self.assertIn("Error code: 400", rv.text)
            self.assertIn("Cache-Control", rv.headers)
            self.assertEqual(rv.headers["Cache-Control"], "no-store")

    def test_401(self):
        with self.client as c:
            rv = c.get("/error/401/")
            self.assertEqual(rv.status_code, 401)
            self.assertIn("Restricted", rv.text)
            self.assertIn("Error code: 401", rv.text)
            self.assertIn("Cache-Control", rv.headers)
            self.assertEqual(rv.headers["Cache-Control"], "no-store")

    def test_403(self):
        with self.client as c:
            rv = c.get("/error/403/")
            self.assertEqual(rv.status_code, 403)
            self.assertIn("Restricted", rv.text)
            self.assertIn("Error code: 403", rv.text)
            self.assertIn("Cache-Control", rv.headers)
            self.assertEqual(rv.headers["Cache-Control"], "no-store")

    def test_404(self):
        with self.client as c:
            rv = c.get("/error/404/")
            self.assertEqual(rv.status_code, 404)
            self.assertIn("Page not found", rv.text)
            self.assertIn("Error code: 404", rv.text)
            self.assertIn("Cache-Control", rv.headers)
            self.assertEqual(rv.headers["Cache-Control"], "no-store")

    def test_405(self):
        with self.client as c:
            rv = c.get("/error/405/")
            self.assertEqual(rv.status_code, 405)
            self.assertIn("The page you requested cannot be served", rv.text)
            self.assertIn("Error code: 405", rv.text)
            self.assertIn("Cache-Control", rv.headers)
            self.assertEqual(rv.headers["Cache-Control"], "no-store")

    def test_406(self):
        with self.client as c:
            rv = c.get("/error/406/")
            self.assertEqual(rv.status_code, 406)
            self.assertIn("The page you requested cannot be served", rv.text)
            self.assertIn("Error code: 406", rv.text)
            self.assertIn("Cache-Control", rv.headers)
            self.assertEqual(rv.headers["Cache-Control"], "no-store")

    def test_407(self):
        with self.client as c:
            rv = c.get("/error/407/")
            self.assertEqual(rv.status_code, 407)
            self.assertIn("Restricted", rv.text)
            self.assertIn("Error code: 407", rv.text)
            self.assertIn("Cache-Control", rv.headers)
            self.assertEqual(rv.headers["Cache-Control"], "no-store")

    def test_414(self):
        with self.client as c:
            rv = c.get("/error/414/")
            self.assertEqual(rv.status_code, 414)
            self.assertIn("The page you requested cannot be served", rv.text)
            self.assertIn("Error code: 414", rv.text)
            self.assertIn("Cache-Control", rv.headers)
            self.assertEqual(rv.headers["Cache-Control"], "no-store")

    def test_429(self):
        with self.client as c:
            rv = c.get("/error/429/")
            self.assertEqual(rv.status_code, 429)
            self.assertIn("Too many requests", rv.text)
            self.assertIn("Error code: 429", rv.text)
            self.assertIn("Cache-Control", rv.headers)
            self.assertEqual(rv.headers["Cache-Control"], "no-store")

    def test_500(self):
        with self.client as c:
            rv = c.get("/error/500/")
            self.assertEqual(rv.status_code, 500)
            self.assertIn("There is a problem with the service", rv.text)
            self.assertIn("Error code: 500", rv.text)
            self.assertIn("Cache-Control", rv.headers)
            self.assertEqual(rv.headers["Cache-Control"], "no-store")

    def test_502(self):
        with self.client as c:
            rv = c.get("/error/502/")
            self.assertEqual(rv.status_code, 502)
            self.assertIn("There is a problem with the service", rv.text)
            self.assertIn("Error code: 502", rv.text)
            self.assertIn("Cache-Control", rv.headers)
            self.assertEqual(rv.headers["Cache-Control"], "no-store")

    def test_503(self):
        with self.client as c:
            rv = c.get("/error/503/")
            self.assertEqual(rv.status_code, 503)
            self.assertIn("Service unavailable", rv.text)
            self.assertIn("Error code: 503", rv.text)
            self.assertIn("Cache-Control", rv.headers)
            self.assertEqual(rv.headers["Cache-Control"], "no-store")

    def test_504(self):
        with self.client as c:
            rv = c.get("/error/504/")
            self.assertEqual(rv.status_code, 504)
            self.assertIn("There is a problem with the service", rv.text)
            self.assertIn("Error code: 504", rv.text)
            self.assertIn("Cache-Control", rv.headers)
            self.assertEqual(rv.headers["Cache-Control"], "no-store")
