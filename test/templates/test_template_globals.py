import unittest

from flask import render_template_string

from app import create_app


class TemplateGlobalsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("config.Test")

    def test_icon_is_available_in_imported_macro(self):
        with self.app.app_context():
            result = render_template_string(
                "{% from 'macros/newsletter.html' import newsletter %}"
                "{{ newsletter() }}"
            )

        self.assertIn('<span class="tna-newsletter__icon">', result)
