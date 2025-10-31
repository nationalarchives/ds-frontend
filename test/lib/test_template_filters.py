import unittest

from app.lib.template_filters import (
    get_url_domain,
    multiline_address_to_single_line,
)


class ContentParserTestCase(unittest.TestCase):

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
