import unittest

from app.lib.content_parser import (
    b_to_strong,
    lists_to_tna_lists,
    strip_wagtail_attributes,
)

from app import create_app


class ContentParserTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("config.Test").test_client()

    def test_strong_tags(self):
        source = "<p>This is <b>bold</b> text.</p>"
        self.assertEqual(
            b_to_strong(source), "<p>This is <strong>bold</strong> text.</p>"
        )
        source2 = '<p>This is <b class="test">bold</b> text.</p>'
        self.assertEqual(
            b_to_strong(source2),
            '<p>This is <strong class="test">bold</strong> text.</p>',
        )

    def test_unordered_lists(self):
        source = "<ul><li>Alpha</li><li>Beta</li></ul>"
        self.assertEqual(
            lists_to_tna_lists(source),
            '<ul class="tna-ul"><li>Alpha</li><li>Beta</li></ul>',
        )

    def test_ordered_lists(self):
        source = "<ol><li>Alpha</li><li>Beta</li></ol>"
        result = lists_to_tna_lists(source)
        self.assertEqual(
            result, '<ol class="tna-ol"><li>Alpha</li><li>Beta</li></ol>'
        )

    def test_strip_wagtail_attributes(self):
        source = '<p data-block-key="11e5b">What might you find in The National Archives? Browse some of our most important and unusual records right here.</p>'
        self.assertEqual(
            strip_wagtail_attributes(source),
            "<p>What might you find in The National Archives? Browse some of our most important and unusual records right here.</p>",
        )
