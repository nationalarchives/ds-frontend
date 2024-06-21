import unittest

from app.lib.content_parser import (
    b_to_strong,
    lists_to_tna_lists,
    strip_wagtail_attributes,
    wagtail_api_table_to_html,
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

    def test_tables(self):
        self.maxDiff = None
        table_block_data = {
            "title": "Title of the table",
            "table": {
                "cell": [],
                "data": [
                    [
                        "First name",
                        "Surname",
                        "Age",
                    ],
                    [
                        "John",
                        "Doe",
                        "50",
                    ],
                    [
                        "Jane",
                        "Doe",
                        "25",
                    ],
                ],
                "mergeCells": [],
                "table_caption": "Ages of members of the Doe family",
                "first_col_is_header": False,
                "table_header_choice": "row",
                "first_row_is_table_header": True,
            },
        }
        with self.app.application.app_context():
            result = wagtail_api_table_to_html(table_block_data["table"])
            self.assertEqual(
                result,
                """<div class="tna-table-wrapper">
  <table class="tna-table">
    <caption class="tna-table__caption">
      Ages of members of the Doe family
    </caption>
    <thead class="tna-table__head">
      <tr class="tna-table__row">
        <th class="tna-table__header">First name</th>
        <th class="tna-table__header">Surname</th>
        <th class="tna-table__header">Age</th>
      </tr>
    </thead>
    <tbody class="tna-table__body">
      <tr class="tna-table__row">
        <td class="tna-table__cell">John</td>
        <td class="tna-table__cell">Doe</td>
        <td class="tna-table__cell">50</td>
      </tr>
      <tr class="tna-table__row">
        <td class="tna-table__cell">Jane</td>
        <td class="tna-table__cell">Doe</td>
        <td class="tna-table__cell">25</td>
      </tr>
    </tbody>
  </table>
</div>""",
            )
