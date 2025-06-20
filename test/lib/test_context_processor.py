import datetime
import unittest

from app.lib.context_processor import pretty_date_range


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

    def test_pretty_date_range_with_time(self):
        start_date = "2000-01-01T12:30:00Z"
        self.assertEqual(
            pretty_date_range(start_date, "2000-01-01T12:30:00Z", show_time=True),
            "1 January 2000, 12:30",
        )
        self.assertEqual(
            pretty_date_range(start_date, "2000-01-01T12:31:00Z", show_time=True),
            "1 January 2000, 12:30 to 12:31",
        )
        self.assertEqual(
            pretty_date_range(start_date, "2000-01-01T23:59:59Z", show_time=True),
            "1 January 2000, 12:30 to 23:59",
        )
        self.assertEqual(
            pretty_date_range(start_date, "2000-01-02T00:00:0Z", show_time=True),
            "1 to 2 January 2000",
        )
        self.assertEqual(
            pretty_date_range(start_date, "2000-01-02T14:45:00Z", show_time=True),
            "1 to 2 January 2000",
        )
        self.assertEqual(
            pretty_date_range(start_date, "2000-01-31T14:45:00Z", show_time=True),
            "1 to 31 January 2000",
        )
        self.assertEqual(
            pretty_date_range(start_date, "2000-02-01T14:45:00Z", show_time=True),
            "1 January to 1 February 2000",
        )
        self.assertEqual(
            pretty_date_range(start_date, "2000-12-31T14:45:00Z", show_time=True),
            "2000",
        )
        self.assertEqual(
            pretty_date_range(start_date, "2001-01-01T14:45:00Z", show_time=True),
            "1 January 2000 to 1 January 2001",
        )
        self.assertEqual(
            pretty_date_range(start_date, "2001-12-31T14:45:00Z", show_time=True),
            "2000 to 2001",
        )
        self.assertEqual(
            pretty_date_range(start_date, None, show_time=True),
            "From 1 January 2000",
        )
        self.assertEqual(
            pretty_date_range(None, "2001-12-31T14:45:00Z", show_time=True),
            "Now to 31 December 2001",
        )
