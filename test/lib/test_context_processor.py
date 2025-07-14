import unittest

from app.lib.context_processor import (
    is_today_in_date_range,
    pretty_date_range,
    pretty_datetime_range,
    pretty_price_range,
)


class ContextParserTestCase(unittest.TestCase):
    def test_pretty_date_range(self):
        start_date = "2000-01-01"
        self.assertEqual(pretty_date_range(start_date, "2000-01-01"), "1 January 2000")
        self.assertEqual(
            pretty_date_range(start_date, "2000-01-02"), "1 to 2 January 2000"
        )
        self.assertEqual(
            pretty_date_range(start_date, "2000-01-31"), "1 to 31 January 2000"
        )
        self.assertEqual(
            pretty_date_range(start_date, "2000-02-01"),
            "1 January to 1 February 2000",
        )
        self.assertEqual(pretty_date_range(start_date, "2000-12-31"), "2000")
        self.assertEqual(
            pretty_date_range(start_date, "2001-01-01"),
            "1 January 2000 to 1 January 2001",
        )
        self.assertEqual(pretty_date_range(start_date, "2001-12-31"), "2000 to 2001")
        self.assertEqual(
            pretty_date_range(None, "2001-12-31"), "Now to 31 December 2001"
        )
        self.assertEqual(pretty_date_range(start_date, None), "From 1 January 2000")

    def test_pretty_date_range_no_days(self):
        start_date = "2000-01-01"
        self.assertEqual(
            pretty_date_range(start_date, "2000-01-01", omit_days=True),
            "January 2000",
        )
        self.assertEqual(
            pretty_date_range(start_date, "2000-01-02", omit_days=True),
            "January 2000",
        )
        self.assertEqual(
            pretty_date_range(start_date, "2000-01-31", omit_days=True),
            "January 2000",
        )
        self.assertEqual(
            pretty_date_range(start_date, "2000-02-01", omit_days=True),
            "January to February 2000",
        )
        self.assertEqual(
            pretty_date_range(start_date, "2000-12-31", omit_days=True), "2000"
        )
        self.assertEqual(
            pretty_date_range(start_date, "2001-01-01", omit_days=True),
            "January 2000 to January 2001",
        )
        self.assertEqual(
            pretty_date_range(start_date, "2001-12-31", omit_days=True),
            "2000 to 2001",
        )
        self.assertEqual(
            pretty_date_range(start_date, None, omit_days=True),
            "From January 2000",
        )
        self.assertEqual(
            pretty_date_range(None, "2001-12-31", omit_days=True),
            "Now to December 2001",
        )

    def test_pretty_datetime_range(self):
        start_date = "2000-01-01T12:30:00Z"
        self.assertEqual(
            pretty_datetime_range(start_date, "2000-01-01T12:30:00Z"),
            "1 January 2000, 12:30",
        )
        self.assertEqual(
            pretty_datetime_range(start_date, "2000-01-01T12:31:00Z"),
            "1 January 2000, 12:30 to 12:31",
        )
        self.assertEqual(
            pretty_datetime_range(start_date, "2000-01-01T23:59:59Z"),
            "1 January 2000, 12:30 to 23:59",
        )
        self.assertEqual(
            pretty_datetime_range(start_date, "2000-01-02T00:00:0Z"),
            "1 January 2000, 12:30 to 2 January 2000, 00:00",
        )
        self.assertEqual(
            pretty_datetime_range(start_date, "2000-01-02T14:45:00Z"),
            "1 January 2000, 12:30 to 2 January 2000, 14:45",
        )
        self.assertEqual(
            pretty_datetime_range(start_date, "2000-01-31T14:45:00Z"),
            "1 January 2000, 12:30 to 31 January 2000, 14:45",
        )
        self.assertEqual(
            pretty_datetime_range(start_date, "2000-02-01T14:45:00Z"),
            "1 January 2000, 12:30 to 1 February 2000, 14:45",
        )
        self.assertEqual(
            pretty_datetime_range(start_date, "2000-12-31T14:45:00Z"),
            "1 January 2000, 12:30 to 31 December 2000, 14:45",
        )
        self.assertEqual(
            pretty_datetime_range(start_date, "2001-01-01T14:45:00Z"),
            "1 January 2000, 12:30 to 1 January 2001, 14:45",
        )
        self.assertEqual(
            pretty_datetime_range(start_date, "2001-12-31T14:45:00Z"),
            "1 January 2000, 12:30 to 31 December 2001, 14:45",
        )
        self.assertEqual(
            pretty_datetime_range(start_date, None),
            "From 1 January 2000, 12:30",
        )
        self.assertEqual(
            pretty_datetime_range(None, "2001-12-31T14:45:00Z"),
            "Now to 31 December 2001, 14:45",
        )

    def test_pretty_price_range(self):
        self.assertEqual(pretty_price_range(0, 0), "Free")
        self.assertEqual(pretty_price_range("0", "0"), "Free")
        self.assertEqual(pretty_price_range(5, 5), "£5")
        self.assertEqual(pretty_price_range("5", 5), "£5")
        self.assertEqual(pretty_price_range(5, "5"), "£5")
        self.assertEqual(pretty_price_range("5", "5"), "£5")
        self.assertEqual(pretty_price_range(5.1, 5.1), "£5.10")
        self.assertEqual(pretty_price_range(0, 5), "Free to £5")
        self.assertEqual(pretty_price_range(None, 5), "Free to £5")
        self.assertEqual(pretty_price_range(5, 0), "From £5")
        self.assertEqual(pretty_price_range(5, 10), "£5 to £10")
        self.assertEqual(pretty_price_range(10, 5), "£5 to £10")
        with self.assertRaises(ValueError):
            pretty_price_range("5", "a")
            pretty_price_range("5", [])
            pretty_price_range("5", True)

    def test_is_today_in_date_range(self):
        self.assertTrue(is_today_in_date_range("2000-01-01", "2999-01-01"))
        self.assertFalse(is_today_in_date_range("2000-01-01", "2001-01-01"))
        self.assertFalse(is_today_in_date_range("2998-01-01", "2999-01-01"))
        self.assertFalse(is_today_in_date_range(None, "2023-10-31"))
        self.assertFalse(is_today_in_date_range("2023-10-01", None))
        self.assertFalse(is_today_in_date_range(None, None))
