import unittest

from app import create_app


class MyAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("config.TestingConfig").test_client()

    def test_greeting(self):
        rv = self.app.get("/browse/")
        print("==========")
        print(rv)
        self.assertEqual(rv.status_code, 200)
        self.assertIn("Explore 1,000 years of history", rv.text)

    def test_404(self):
        rv = self.app.get("/foobar/")
        self.assertEqual(rv.status_code, 404)
