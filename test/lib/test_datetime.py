import unittest

from app.lib.datetime import group_items_by_year_and_month


class DateTimeTestCase(unittest.TestCase):
    def test_group_items_by_year_and_month(self):
        input_data = [
            {"id": 1, "date": "2022-05-15"},
            {"id": 2, "date": "2022-05-20"},
            {"id": 3, "date": "2022-06-10"},
            {"id": 4, "date": "2021-12-25"},
            {"id": 5, "date": "2021-11-11"},
            {"id": 6, "date": "2022-06-15"},
        ]
        result = group_items_by_year_and_month({"items": input_data}, "date")
        expected = [
            {
                "heading": "2022",
                "items": [
                    {
                        "heading": "May",
                        "items": [
                            {"id": 1, "date": "2022-05-15"},
                            {"id": 2, "date": "2022-05-20"},
                        ],
                    },
                    {
                        "heading": "June",
                        "items": [
                            {"id": 3, "date": "2022-06-10"},
                            {"id": 6, "date": "2022-06-15"},
                        ],
                    },
                ],
            },
            {
                "heading": "2021",
                "items": [
                    {
                        "heading": "December",
                        "items": [{"id": 4, "date": "2021-12-25"}],
                    },
                    {
                        "heading": "November",
                        "items": [{"id": 5, "date": "2021-11-11"}],
                    },
                ],
            },
        ]
        self.assertEqual(result, expected)
