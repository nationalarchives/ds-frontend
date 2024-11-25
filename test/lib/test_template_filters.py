import unittest

from app.lib.template_filters import qs_active, qs_toggler


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
