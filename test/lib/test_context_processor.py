import datetime
import unittest

from app.lib.context_processor import pretty_date_range


class ContextParserTestCase(unittest.TestCase):
    def test_pretty_date_range(self):
        start_date = "2000-01-01"
        self.assertEqual(pretty_date_range(start_date, ""), "From 1 January 2000")
        self.assertEqual(pretty_date_range(start_date, "2000-01-01"), "1 January 2000")
        self.assertEqual(
            pretty_date_range(start_date, "2000-01-02"), "1–2 January 2000"
        )
        self.assertEqual(
            pretty_date_range(start_date, "2000-01-31"), "1–31 January 2000"
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
        self.assertEqual(pretty_date_range(start_date, "2001-12-31"), "2000–2001")

    def test_pretty_date_range_with_time(self):
        start_date = "2000-01-01T13:30:00"
        self.assertEqual(
            pretty_date_range(start_date, ""), "From 1 January 2000, 13:30"
        )
        self.assertEqual(
            pretty_date_range(start_date, "2000-01-01T15:00:00"),
            "1 January 2000, 13:30–15:00",
        )
        self.assertEqual(
            pretty_date_range(start_date, "2000-01-02T15:00:00"),
            "1 January, 13:30 to 2 January 2000, 15:00",
        )
        self.assertEqual(
            pretty_date_range(start_date, "2000-01-31T15:00:00"),
            "1 January, 13:30 to 31 January 2000, 15:00",
        )
        self.assertEqual(
            pretty_date_range(start_date, "2000-02-01T15:00:00"),
            "1 January, 13:30 to 1 February 2000, 15:00",
        )
        self.assertEqual(
            pretty_date_range(start_date, "2000-12-31T15:00:00"),
            "1 January, 13:30 to 31 December 2000, 15:00",
        )
        self.assertEqual(
            pretty_date_range(start_date, "2001-01-01T15:00:00"),
            "1 January 2000, 13:30 to 1 January 2001, 15:00",
        )
        self.assertEqual(
            pretty_date_range(start_date, "2001-12-31T15:00:00"), "2000–2001"
        )

    def test_pretty_date_range_no_days(self):
        start_date = "2000-01-01"
        self.assertEqual(
            pretty_date_range(start_date, "2000-01-01", False), "January 2000"
        )
        self.assertEqual(
            pretty_date_range(start_date, "2000-01-02", False), "January 2000"
        )
        self.assertEqual(
            pretty_date_range(start_date, "2000-01-31", False), "January 2000"
        )
        self.assertEqual(
            pretty_date_range(start_date, "2000-02-01", False),
            "January to February 2000",
        )
        self.assertEqual(pretty_date_range(start_date, "2000-12-31", False), "2000")
        self.assertEqual(
            pretty_date_range(start_date, "2001-01-01", False),
            "January 2000 to January 2001",
        )
        self.assertEqual(
            pretty_date_range(start_date, "2001-12-31", False), "2000–2001"
        )
