import unittest

from app.lib.template_filters import (
    currency,
    get_url_domain,
    multiline_address_to_single_line,
    pretty_date,
    pretty_price,
    qs_active,
    qs_toggler,
    seconds_to_iso_8601_duration,
    seconds_to_time,
    slugify,
    unslugify,
)


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
        self.assertFalse(qs_active(TEST_QS, "c", ""))
        self.assertFalse(qs_active(TEST_QS, "a", ""))
        self.assertFalse(qs_active(TEST_QS, "", ""))
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
        self.assertEqual(
            pretty_date("2000-01-01T12:30:00Z", show_day=True, show_time=True),
            "Saturday 1 January 2000, 12:30",
        )

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

    def test_seconds_to_time(self):
        self.assertEqual(seconds_to_time(0), "00h 00m 00s")
        self.assertEqual(seconds_to_time(1), "00h 00m 01s")
        self.assertEqual(seconds_to_time(59), "00h 00m 59s")
        self.assertEqual(seconds_to_time(60), "00h 01m 00s")
        self.assertEqual(seconds_to_time(61), "00h 01m 01s")
        self.assertEqual(seconds_to_time(3599), "00h 59m 59s")
        self.assertEqual(seconds_to_time(3600), "01h 00m 00s")
        self.assertEqual(seconds_to_time(3601), "01h 00m 01s")

    def test_seconds_to_iso_8601_duration(self):
        self.assertEqual(seconds_to_iso_8601_duration(0), "PT0S")
        self.assertEqual(seconds_to_iso_8601_duration(1), "PT1S")
        self.assertEqual(seconds_to_iso_8601_duration(59), "PT59S")
        self.assertEqual(seconds_to_iso_8601_duration(60), "PT1M0S")
        self.assertEqual(seconds_to_iso_8601_duration(61), "PT1M1S")
        self.assertEqual(seconds_to_iso_8601_duration(3599), "PT59M59S")
        self.assertEqual(seconds_to_iso_8601_duration(3600), "PT1H0M0S")
        self.assertEqual(seconds_to_iso_8601_duration(3601), "PT1H0M1S")

    def test_slugify(self):
        self.assertEqual(slugify(""), "")
        self.assertEqual(slugify("test"), "test")
        self.assertEqual(slugify("  test TEST"), "test-test")
        self.assertEqual(slugify("test 12 3 -4 "), "test-12-3-4")
        self.assertEqual(slugify("test---test"), "test-test")
        self.assertEqual(slugify("test---"), "test")
        self.assertEqual(slugify("test---$"), "test")
        self.assertEqual(slugify("test---$---"), "test")

    def test_unslugify(self):
        self.assertEqual(unslugify("test-test"), "Test test")
        self.assertEqual(unslugify("test-test", False), "test test")
        self.assertEqual(unslugify("test-123"), "Test 123")
        self.assertEqual(unslugify("test-1-2-3"), "Test 1 2 3")

    def test_pretty_price(self):
        self.assertEqual(pretty_price(0), "Free")
        self.assertEqual(pretty_price("0"), "Free")
        self.assertEqual(pretty_price(0.1), "£0.10")
        self.assertEqual(pretty_price("0.1"), "£0.10")
        self.assertEqual(pretty_price("0.10"), "£0.10")
        self.assertEqual(pretty_price("0.101"), "£0.10")
        self.assertEqual(pretty_price("0.001"), "£0.00")
        self.assertEqual(pretty_price("0.009"), "£0.01")
        self.assertEqual(pretty_price("1"), "£1")
        self.assertEqual(pretty_price("01"), "£1")
        self.assertEqual(pretty_price("1.1"), "£1.10")
        self.assertEqual(pretty_price("1.11"), "£1.11")
        self.assertEqual(pretty_price("1.111"), "£1.11")
        self.assertEqual(pretty_price("123456789"), "£123,456,789")
        self.assertEqual(pretty_price("123456789.01"), "£123,456,789.01")

    def test_get_url_domain(self):
        self.assertEqual(
            get_url_domain(
                "https://www.nationalarchives.gov.uk/explore-the-collection/stories/john-blanke/"
            ),
            "nationalarchives.gov.uk",
        )
        self.assertEqual(
            get_url_domain(
                "https://discovery.nationalarchives.gov.uk/results/r?_q=ufo&_sd=&_ed=&_hb="
            ),
            "discovery.nationalarchives.gov.uk",
        )

    def test_multiline_address_to_single_line(self):
        self.assertEqual(
            multiline_address_to_single_line(
                '<p data-block-key="ovqe3">Somewhere</p><p data-block-key="52qj4">123 Road Street</p><p data-block-key="6ro70">Devon,<br/>UK</p><p data-block-key="5n2cs">PL4 7EX</p>'
            ),
            "Somewhere, 123 Road Street, Devon, UK, PL4 7EX",
        )
