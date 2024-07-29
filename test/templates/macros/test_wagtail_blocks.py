import unittest

from flask import render_template_string

from app import create_app


class ContentParserTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("config.Test").test_client()

    def test_tables(self):
        self.maxDiff = None
        table_block_data = {
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
            result = render_template_string(
                "{% from 'macros/wagtail_blocks/table.html' import wagtailTable %}"
                "{{ wagtailTable(table_block_data) }}",
                table_block_data=table_block_data,
            )
            self.assertEqual(
                result,
                """  <div class="tna-table-wrapper">
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
  </div>
""",
            )
