import json
import unittest

import requests_mock

from app import create_app


class GeneralWagtailTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("config.Test").test_client()
        self.domain = "http://localhost"
        self.mock_api_url = self.app.application.config["WAGTAIL_API_URL"]

    def test_no_api_response(self):
        rv = self.app.get("/foobar/")
        self.assertEqual(rv.status_code, 502)
        self.assertIn(
            '<h1 class="tna-heading-xl">An error occured with our system</h1>',
            rv.text,
        )

    @requests_mock.Mocker()
    def test_page_not_found(self, m):
        mock_endpoint = (
            f"{self.mock_api_url}/pages/find/?html_path=foobar&format=json"
        )
        mock_respsone = {"message": "not found"}
        m.get(mock_endpoint, json=mock_respsone, status_code=404)
        rv = self.app.get("/foobar/")
        self.assertEqual(rv.status_code, 404)
        self.assertIn(
            '<h1 class="tna-heading-xl">Page not found</h1>',
            rv.text,
        )
