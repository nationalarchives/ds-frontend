import unittest

from app.lib.datetime import get_date_from_string, group_items_by_year_and_month


class DateTimeTestCase(unittest.TestCase):
    def test_get_date_from_string(self):
        self.assertEqual(
            get_date_from_string("2006-05-04").isoformat(), "2006-05-04T00:00:00"
        )
        self.assertEqual(
            get_date_from_string("2006-05").isoformat(), "2006-05-01T00:00:00"
        )
        self.assertEqual(
            get_date_from_string("2006").isoformat(), "2006-01-01T00:00:00"
        )
        self.assertEqual(
            get_date_from_string("2006-05-04T01:02:03.999Z").isoformat(),
            "2006-05-04T01:02:03.999000+00:00",
        )
        self.assertEqual(
            get_date_from_string("2006-05-04T01:02:03Z").isoformat(),
            "2006-05-04T01:02:03+00:00",
        )
        self.assertEqual(
            get_date_from_string("2006-05-04T01:02:03+0100").isoformat(),
            "2006-05-04T01:02:03+01:00",
        )
        self.assertEqual(
            get_date_from_string("1000").isoformat(), "1000-01-01T00:00:00"
        )
        self.assertEqual(get_date_from_string("2006-12-32"), None)
        self.assertEqual(get_date_from_string("2006-13"), None)
        self.assertEqual(get_date_from_string("999"), None)
        self.assertEqual(get_date_from_string("06"), None)
        self.assertEqual(get_date_from_string("00"), None)
        self.assertEqual(get_date_from_string("99"), None)
        self.assertEqual(get_date_from_string("9"), None)
        self.assertEqual(get_date_from_string("abc"), None)
        self.assertEqual(get_date_from_string(""), None)
        self.assertEqual(get_date_from_string(None), None)
        self.assertEqual(get_date_from_string(False), None)

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
