"""Unit tests for DOI utility functions in metrics/util.py."""

import unittest

from metrics.util import is_DOI, get_DOI


class TestIsDOI(unittest.TestCase):
    """Tests for is_DOI()."""

    # --- Valid DOIs (raw) ---
    def test_raw_doi_simple(self):
        self.assertTrue(is_DOI("10.1038/s41586-020-2649-2"))

    def test_raw_doi_uppercase_suffix(self):
        self.assertTrue(is_DOI("10.1126/SCIENCE.97.2524.434"))

    def test_raw_doi_long_registrant(self):
        self.assertTrue(is_DOI("10.15454/P27LDX"))

    def test_raw_doi_with_colon_in_suffix(self):
        self.assertTrue(is_DOI("10.1186/s13326-023-00289-5"))

    # --- Valid DOIs (URL forms) ---
    def test_https_doi_org_url(self):
        self.assertTrue(is_DOI("https://doi.org/10.1038/s41586-020-2649-2"))

    def test_http_doi_org_url(self):
        self.assertTrue(is_DOI("http://doi.org/10.1038/s41586-020-2649-2"))

    def test_dx_doi_org_url(self):
        self.assertTrue(is_DOI("https://dx.doi.org/10.1126/SCIENCE.97.2524.434"))

    def test_doi_org_url_encoded(self):
        self.assertTrue(is_DOI("https://doi.org/10.1038/s41586%2D020%2D2649%2D2"))

    # --- Invalid inputs ---
    def test_plain_url_not_doi(self):
        self.assertFalse(is_DOI("https://example.org/not-a-doi"))

    def test_random_string(self):
        self.assertFalse(is_DOI("this is not a doi"))

    def test_doi_org_without_prefix(self):
        # doi.org URL without a valid DOI path
        self.assertFalse(is_DOI("https://doi.org/just-a-path"))

    def test_empty_string(self):
        self.assertFalse(is_DOI(""))

    def test_partial_doi_no_suffix(self):
        # registrant code present but no suffix
        self.assertFalse(is_DOI("10.1038/"))

    def test_wrong_prefix(self):
        self.assertFalse(is_DOI("12.1038/s41586-020-2649-2"))


class TestGetDOI(unittest.TestCase):
    """Tests for get_DOI()."""

    # --- Extraction from raw DOI ---
    def test_raw_doi_returns_doi(self):
        self.assertEqual(
            get_DOI("10.1038/s41586-020-2649-2"), "10.1038/s41586-020-2649-2"
        )

    def test_raw_doi_uppercase(self):
        self.assertEqual(
            get_DOI("10.1126/SCIENCE.97.2524.434"), "10.1126/SCIENCE.97.2524.434"
        )

    # --- Extraction from doi.org URLs ---
    def test_https_doi_org_extracts_doi(self):
        self.assertEqual(
            get_DOI("https://doi.org/10.1038/s41586-020-2649-2"),
            "10.1038/s41586-020-2649-2",
        )

    def test_http_doi_org_extracts_doi(self):
        self.assertEqual(
            get_DOI("http://doi.org/10.1186/s13326-023-00289-5"),
            "10.1186/s13326-023-00289-5",
        )

    def test_dx_doi_org_extracts_doi(self):
        self.assertEqual(
            get_DOI("https://dx.doi.org/10.1126/SCIENCE.97.2524.434"),
            "10.1126/SCIENCE.97.2524.434",
        )

    def test_url_encoded_doi_decoded(self):
        result = get_DOI("https://doi.org/10.1038/s41586%2D020%2D2649%2D2")
        self.assertEqual(result, "10.1038/s41586-020-2649-2")

    # --- Non-DOI inputs must NOT crash and must return None ---
    def test_non_doi_url_returns_none(self):
        self.assertIsNone(get_DOI("https://example.org/not-a-doi"))

    def test_random_string_returns_none(self):
        self.assertIsNone(get_DOI("this is not a doi at all"))

    def test_empty_string_returns_none(self):
        self.assertIsNone(get_DOI(""))

    def test_doi_org_bad_path_returns_none(self):
        self.assertIsNone(get_DOI("https://doi.org/just-a-path"))


if __name__ == "__main__":
    unittest.main()
