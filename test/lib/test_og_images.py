import unittest
from unittest.mock import patch

import requests_mock

from app import create_app
from app.lib.og_images import generate_external_og_image


class ExternalOgImageTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("config.Test")
        self.content_url = self.app.config["OG_CONTENT_BASE_URL"]

    def generate_image(self):
        with (
            self.app.app_context(),
            patch("app.lib.og_images.generate_og_image") as generate_og_image,
        ):
            generate_external_og_image("example-page")
        return generate_og_image

    @requests_mock.Mocker()
    def test_uses_og_title_and_og_description_first(self, mocker):
        mocker.get(
            f"{self.content_url}/example-page/",
            text="""
                <html>
                    <head>
                        <meta property="og:title" content="OG title">
                        <meta property="og:description" content="OG description">
                        <meta name="description" content="Meta description">
                        <title>Document title</title>
                    </head>
                    <body><h1>Heading title</h1></body>
                </html>
            """,
        )

        generate_og_image = self.generate_image()

        generate_og_image.assert_called_once_with(
            None,
            "OG title",
            "OG description",
            self.app.config["OG_DEFAULT_IMAGE"],
        )

    @requests_mock.Mocker()
    def test_uses_h1_when_og_title_is_missing(self, mocker):
        mocker.get(
            f"{self.content_url}/example-page/",
            text="""
                <h1>Heading title</h1>
                <meta property="og:description" content="OG description">
            """,
        )

        generate_og_image = self.generate_image()

        generate_og_image.assert_called_once_with(
            None,
            "Heading title",
            "OG description",
            self.app.config["OG_DEFAULT_IMAGE"],
        )

    @requests_mock.Mocker()
    def test_uses_document_title_when_og_title_and_h1_are_missing(self, mocker):
        mocker.get(
            f"{self.content_url}/example-page/",
            text="""
                <title>Document title</title>
                <meta property="og:description" content="OG description">
            """,
        )

        generate_og_image = self.generate_image()

        generate_og_image.assert_called_once_with(
            None,
            "Document title",
            "OG description",
            self.app.config["OG_DEFAULT_IMAGE"],
        )

    @requests_mock.Mocker()
    def test_uses_meta_description_when_og_description_is_missing(self, mocker):
        mocker.get(
            f"{self.content_url}/example-page/",
            text="""
                <title>Document title</title>
                <meta name="description" content="Meta description">
            """,
        )

        generate_og_image = self.generate_image()

        generate_og_image.assert_called_once_with(
            None,
            "Document title",
            "Meta description",
            self.app.config["OG_DEFAULT_IMAGE"],
        )

    @requests_mock.Mocker()
    def test_uses_supertitle_paragraph_in_hgroup(self, mocker):
        mocker.get(
            f"{self.content_url}/example-page/",
            text="""
                <hgroup class="tna-hgroup-xl">
                    <p class="tna-hgroup__supertitle">Collection</p>
                    <h1 class="tna-hgroup__title">Page title</h1>
                </hgroup>
                <meta property="og:description" content="Page description">
            """,
        )

        generate_og_image = self.generate_image()

        generate_og_image.assert_called_once_with(
            "Collection",
            "Page title",
            "Page description",
            self.app.config["OG_DEFAULT_IMAGE"],
        )

    @requests_mock.Mocker()
    def test_uses_supertitle_span_in_hgroup(self, mocker):
        mocker.get(
            f"{self.content_url}/example-page/",
            text="""
                <hgroup class="tna-hgroup-xl">
                    <h1>
                        <span class="tna-hgroup__supertitle">Event</span>
                        <span class="tna-hgroup__title">Page title</span>
                    </h1>
                </hgroup>
                <meta property="og:description" content="Page description">
            """,
        )

        generate_og_image = self.generate_image()

        generate_og_image.assert_called_once_with(
            "Event",
            "Event Page title",
            "Page description",
            self.app.config["OG_DEFAULT_IMAGE"],
        )

    @requests_mock.Mocker()
    def test_ignores_supertitle_outside_hgroup(self, mocker):
        mocker.get(
            f"{self.content_url}/example-page/",
            text="""
                <p class="tna-hgroup__supertitle">Not a supertitle</p>
                <h1>Page title</h1>
                <meta property="og:description" content="Page description">
            """,
        )

        generate_og_image = self.generate_image()

        generate_og_image.assert_called_once_with(
            None,
            "Page title",
            "Page description",
            self.app.config["OG_DEFAULT_IMAGE"],
        )
