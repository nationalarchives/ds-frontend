import json
import unittest

import requests_mock

from app import create_app


class ArticleTemplateTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("config.Test").test_client()
        self.domain = "http://localhost"
        self.mock_api_url = self.app.application.config["WAGTAIL_API_URL"]

    @requests_mock.Mocker()
    def test_template(self, m):
        with open(
            "tmp/ds-wagtail/etna/api/tests/expected_results/article.json", "r"
        ) as json_file:
            json_file_contents = json_file.read()
            json_file.close()
            page_data_json = (
                json_file_contents.replace("ARTICLE_ID", "2")
                .replace("ARTICLE_INDEX_ID", "1")
                .replace("FOCUSED_ID", "3")
                .replace("ARTS_ID", "4")
                .replace("EARLY_MODERN_ID", "5")
                .replace("POSTWAR_ID", "6")
            )
            page_data = json.loads(page_data_json)
            mock_endpoint_slug = "test-article"
            mock_endpoint = f"{self.mock_api_url}/pages/find/?html_path={mock_endpoint_slug}&format=json"
            m.get(mock_endpoint, json=page_data)
            rv = self.app.get(f"/{mock_endpoint_slug}/")
            self.assertEqual(rv.status_code, 200)
            self.assertIn(
                f"<title>{page_data['title']} - The National Archives</title>",
                rv.text,
            )
            self.assertIn(
                f"<meta name=\"tna.page.wagtail.id\" content=\"{page_data['id']}\">",
                rv.text,
            )
            self.assertIn(
                f"<meta name=\"tna.page.wagtail.title\" content=\"{page_data['title']}\">",
                rv.text,
            )
            self.assertIn(
                f"<meta name=\"tna.page.wagtail.type\" content=\"{page_data['meta']['type']}\">",
                rv.text,
            )
            self.assertIn(
                f"<meta name=\"tna.page.tags\" content=\"{';'.join(page_data['tags'])}\">",
                rv.text,
            )
            # self.assertIn('<meta name="description" content="articles.ArticlePage">', rv.text)
            self.assertIn(
                '<p class="tna-hgroup__supertitle">The story of</p>',
                rv.text,
            )
            self.assertIn(
                f"<h1 class=\"tna-hgroup__title\" itemprop=\"name\">{page_data['title']}</h1>",
                rv.text,
            )
