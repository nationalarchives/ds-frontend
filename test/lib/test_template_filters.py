import unittest

from app.lib.template_filters import (
    domain_from_url,
    headings_list,
    key_stage_ranges,
    multiline_address_to_single_line,
    supertitle_from_domain,
)


class ContentParserTestCase(unittest.TestCase):
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
                '<h1 id="intro">Introduction <span>HIDDEN</span></h1>'
                '<h2 id="section-a">Section A <span>HIDDEN <span>HIDDEN</span></span></h2>'
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
                '<h2 id="section-a">Section A <span>HIDDEN <span>HIDDEN</span></span></h2>'
                '<h3 id="sub-a">Sub section A</h3>'
                '<h4 id="sub-a-a">Sub sub section A</h4>'
                '<h4 id="sub-a-b">Sub sub section B <span>HIDDEN <span>HIDDEN</span></span></h4>'
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
