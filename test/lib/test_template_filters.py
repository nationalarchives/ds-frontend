import unittest

from app.lib.template_filters import currency, pretty_date, qs_active, qs_toggler


class ContentParserTestCase(unittest.TestCase):
    def test_jinja_filters_qs_toggler(self):
        TEST_QS = {"a": "1", "b": "2"}
        # Adds a new qs
        self.assertEqual("a=1&b=2&c=3", qs_toggler(TEST_QS.copy(), "c", "3"))
        # Changes an existing qs
        self.assertEqual("a=1&b=1", qs_toggler(TEST_QS.copy(), "b", "1"))
        # Removes a qs of the same value.
        self.assertEqual("b=2", qs_toggler(TEST_QS.copy(), "a", "1"))
        # Handle empty existing qs
        self.assertEqual("a=1", qs_toggler({}, "a", "1"))

    def test_jinja_filters_qs_active(self):
        TEST_QS = {"a": "1", "b": "2"}
        self.assertTrue(qs_active(TEST_QS, "a", "1"))
        self.assertTrue(qs_active(TEST_QS, "b", "2"))
        self.assertFalse(qs_active(TEST_QS, "a", "2"))
        self.assertFalse(qs_active(TEST_QS, "b", "1"))
        self.assertFalse(qs_active(TEST_QS, "c", "3"))
        # Handles empty query strings
        self.assertFalse(qs_active({}, "a", "1"))
        self.assertFalse(qs_active({}, "", ""))
        self.assertFalse(qs_active({"a": "1"}, "", ""))

    def test_pretty_date(self):
        self.assertEqual(pretty_date("2000-01-01T12:00:00Z"), "1 January 2000")
        self.assertEqual(pretty_date("2000-01-01"), "1 January 2000")
        self.assertEqual(pretty_date("2000-12-31"), "31 December 2000")
        self.assertEqual(pretty_date("2000-01"), "January 2000")
        self.assertEqual(pretty_date("2000"), "2000")
        self.assertEqual(
            pretty_date("2000-01-01T12:00:00Z", show_day=True),
            "Saturday 1 January 2000",
        )
        self.assertEqual(
            pretty_date("2000-01-01", show_day=True), "Saturday 1 January 2000"
        )
        self.assertEqual(
            pretty_date("2000-12-31", show_day=True), "Sunday 31 December 2000"
        )
        self.assertEqual(pretty_date("2000-01", show_day=True), "January 2000")
        self.assertEqual(pretty_date("2000", show_day=True), "2000")

    def test_currency(self):
        self.assertEqual(currency(0), "0")
        self.assertEqual(currency(5), "5")
        self.assertEqual(currency(5.0), "5")
        self.assertEqual(currency(5.00), "5")
        self.assertEqual(currency(5.1), "5.10")
        self.assertEqual(currency(5.01), "5.01")
        self.assertEqual(currency(5.001), "5.00")
        self.assertEqual(currency(5.005), "5.00")
        self.assertEqual(currency(5.006), "5.01")
        self.assertEqual(currency("0"), "0")
        self.assertEqual(currency("5"), "5")
        self.assertEqual(currency("5.0"), "5")
        self.assertEqual(currency("5.00"), "5")
        self.assertEqual(currency("5.1"), "5.10")
        self.assertEqual(currency("5.01"), "5.01")
        self.assertEqual(currency("5.001"), "5.00")
        self.assertEqual(currency("5.005"), "5.00")
        self.assertEqual(currency("5.006"), "5.01")
