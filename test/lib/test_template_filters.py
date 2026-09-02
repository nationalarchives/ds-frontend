import unittest
from datetime import datetime, timedelta, timezone

from app.lib.template_filters import (
    currency,
    domain_from_url,
    headings_list,
    is_today_or_future,
    key_stage_ranges,
    multiline_address_to_single_line,
    pretty_date,
    pretty_price,
    seconds_to_iso_8601_duration,
    seconds_to_time,
    supertitle_from_domain,
)


class ContentParserTestCase(unittest.TestCase):
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

    def test_is_today_or_future(self):
        self.assertTrue(is_today_or_future("2999-01-01"))
        self.assertFalse(is_today_or_future("2000-01-01"))
        today = datetime.now(tz=timezone.utc).date()
        self.assertTrue(is_today_or_future(today.isoformat()))
        tomorrow = today + timedelta(days=1)
        self.assertTrue(
            is_today_or_future(f"{tomorrow.year}-{tomorrow.month}-{tomorrow.day}")
        )
        yesterday = today + timedelta(days=-1)
        self.assertFalse(
            is_today_or_future(f"{yesterday.year}-{yesterday.month}-{yesterday.day}")
        )
        self.assertFalse(is_today_or_future(None))

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

    def test_domain_from_url(self):
        self.assertEqual(
            domain_from_url(
                "https://www.nationalarchives.gov.uk/explore-the-collection/stories/john-blanke/"
            ),
            "nationalarchives.gov.uk",
        )
        self.assertEqual(
            domain_from_url(
                "https://discovery.nationalarchives.gov.uk/results/r?_q=ufo&_sd=&_ed=&_hb="
            ),
            "discovery.nationalarchives.gov.uk",
        )

    def test_supertitle_from_domain(self):
        self.assertEqual(
            supertitle_from_domain(
                "https://www.nationalarchives.gov.uk/explore-the-collection/stories/john-blanke/"
            ),
            "",
        )
        self.assertEqual(
            supertitle_from_domain(
                "https://discovery.nationalarchives.gov.uk/results/r?_q=ufo&_sd=&_ed=&_hb="
            ),
            "",
        )
        self.assertEqual(
            supertitle_from_domain(
                "https://webarchive.nationalarchives.gov.uk/ukgwa/20210201171307/https://alpha.nationalarchives.gov.uk/"
            ),
            "Archived page",
        )
        self.assertEqual(
            supertitle_from_domain(
                "https://webarchive.nationalarchives.gov.uk/ukgwa/https://alpha.nationalarchives.gov.uk/"
            ),
            "Archived page",
        )
        self.assertEqual(
            supertitle_from_domain(
                "https://webarchive.nationalarchives.gov.uk/ukgwa/+/https://alpha.nationalarchives.gov.uk/"
            ),
            "Archived page",
        )
        self.assertEqual(
            supertitle_from_domain("https://webarchive.nationalarchives.gov.uk/ukgwa/"),
            "",
        )
        self.assertEqual(
            supertitle_from_domain("https://github.com/nationalarchives/"),
            "github.com",
        )

    def test_multiline_address_to_single_line(self):
        self.assertEqual(
            multiline_address_to_single_line(
                '<p data-block-key="ovqe3">Somewhere</p><p data-block-key="52qj4">123 Road Street</p><p data-block-key="6ro70">Devon,<br/>UK</p><p data-block-key="5n2cs">PL4 7EX</p>'
            ),
            "Somewhere, 123 Road Street, Devon, UK, PL4 7EX",
        )

    def test_headings_list(self):
        self.maxDiff = None
        self.assertEqual(
            headings_list(
                '<h1 id="intro">Introduction</h1>'
                '<h2 id="section-a">Section A</h2>'
                '<h3 id="sub-a">Sub section A</h3>'
                '<h4 id="sub-a-a">Sub sub section A</h4>'
                '<h4 id="sub-a-b">Sub sub section B</h4>'
                '<h2 id="section-b">Section B</h2>'
                '<h4 id="sub-b-a">Sub sub section A</h4>'
                '<h5 id="sub-b-b">Sub sub sub section B</h5>'
                '<h6 id="sub-b-c">Sub sub sub sub section C</h6>'
            ),
            [
                {
                    "text": "Introduction",
                    "href": "#intro",
                    "level": 1,
                    "children": [
                        {
                            "text": "Section A",
                            "href": "#section-a",
                            "level": 2,
                            "children": [
                                {
                                    "text": "Sub section A",
                                    "href": "#sub-a",
                                    "level": 3,
                                    "children": [
                                        {
                                            "text": "Sub sub section A",
                                            "href": "#sub-a-a",
                                            "level": 4,
                                            "children": [],
                                        },
                                        {
                                            "text": "Sub sub section B",
                                            "href": "#sub-a-b",
                                            "level": 4,
                                            "children": [],
                                        },
                                    ],
                                }
                            ],
                        },
                        {
                            "text": "Section B",
                            "href": "#section-b",
                            "level": 2,
                            "children": [],
                        },
                    ],
                }
            ],
        )

        self.assertEqual(
            headings_list(
                '<h4 id="pre">Pre h1</h4>'
                '<h5 id="non-valid">Sub sub sub section A</h5>'
                '<h2 id="section-a">Section A</h2>'
                '<h3 id="sub-a">Sub section A</h3>'
                '<h4 id="sub-a-a">Sub sub section A</h4>'
                '<h4 id="sub-a-b">Sub sub section B</h4>'
                '<h2 id="section-b">Section B</h2>'
                '<h4 id="sub-b-a">Sub sub section A</h4>'
            ),
            [
                {
                    "text": "Section A",
                    "href": "#section-a",
                    "level": 2,
                    "children": [
                        {
                            "text": "Sub section A",
                            "href": "#sub-a",
                            "level": 3,
                            "children": [
                                {
                                    "text": "Sub sub section A",
                                    "href": "#sub-a-a",
                                    "level": 4,
                                    "children": [],
                                },
                                {
                                    "text": "Sub sub section B",
                                    "href": "#sub-a-b",
                                    "level": 4,
                                    "children": [],
                                },
                            ],
                        }
                    ],
                },
                {
                    "text": "Section B",
                    "href": "#section-b",
                    "level": 2,
                    "children": [],
                },
            ],
        )

        self.assertEqual(
            headings_list('<h2 id="first">First</h2><h2 id="second">Second</h2>'),
            [
                {
                    "text": "First",
                    "href": "#first",
                    "level": 2,
                    "children": [],
                },
                {
                    "text": "Second",
                    "href": "#second",
                    "level": 2,
                    "children": [],
                },
            ],
        )

    def test_key_stage_ranges(self):
        self.assertEqual(key_stage_ranges([1, 2, 3]), ["KS1–⁠KS3"])
        self.assertEqual(key_stage_ranges([1, 2, 4]), ["KS1–⁠KS2", "KS4"])
        self.assertEqual(key_stage_ranges([1, 3, 5]), ["KS1", "KS3", "KS5"])
        self.assertEqual(key_stage_ranges([1, 2, 3, 5]), ["KS1–⁠KS3", "KS5"])
        self.assertEqual(key_stage_ranges([1, 3, 4]), ["KS1", "KS3–⁠KS4"])
        self.assertEqual(key_stage_ranges([4, 1, 3]), ["KS1", "KS3–⁠KS4"])
        self.assertEqual(key_stage_ranges([0, 1, 2]), ["KS1–⁠KS2"])
        self.assertEqual(
            key_stage_ranges([1, 2, 4, 5, 7, 8]), ["KS1–⁠KS2", "KS4–⁠KS5", "KS7–⁠KS8"]
        )

    def test_key_stage_ranges_with_bad_values(self):
        self.assertEqual(key_stage_ranges([]), [])
        self.assertEqual(
            key_stage_ranges([1, 0, None, "a", False, [], {}, 2]), ["KS1–⁠KS2"]
        )
        self.assertEqual(key_stage_ranges([None, 1, 2]), ["KS1–⁠KS2"])
