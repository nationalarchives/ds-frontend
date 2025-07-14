import unittest

from app.lib.datetime import get_date_from_string


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
