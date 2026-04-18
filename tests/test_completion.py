"""Test path completion and fuzzy matching."""

import pytest

from pq.completion import FuzzyMatcher, PathExtractor


@pytest.fixture
def matcher(test_data):
    """Create FuzzyMatcher from test data."""
    extractor = PathExtractor(test_data)
    return FuzzyMatcher(extractor.get_paths())


class TestPathExtraction:
    def test_extract_paths(self, test_data):
        extractor = PathExtractor(test_data)
        paths = extractor.get_paths()
        assert len(paths) > 0
        assert "_['items']" in paths
        assert "_['metadata']" in paths


class TestFuzzyMatching:
    def test_match_name_via_path(self, matcher):
        matches = matcher.find_matches("name")
        assert isinstance(matches, list)

    def test_match_items_via_path(self, matcher):
        matches = matcher.find_matches("items")
        assert isinstance(matches, list)

    def test_match_empty_query(self, matcher):
        matches = matcher.find_matches("")
        assert len(matches) > 0

    def test_match_metadata_via_path(self, matcher):
        matches = matcher.find_matches("metadata")
        assert isinstance(matches, list)


class TestNextLevelSuggestions:
    def test_empty_query_shows_top_level(self, matcher):
        matches = matcher.find_matches("_")
        assert "_['items']" in matches
        assert "_['metadata']" in matches
        assert all(matcher._get_path_depth(m) == 1 for m in matches)

    def test_complete_key_shows_array_indices(self, matcher):
        matches = matcher.find_matches("_['items']")
        assert "_['items'][0]" in matches
        assert "_['items'][1]" in matches
        assert "_['items'][2]" in matches
        assert all(matcher._get_path_depth(m) == 2 for m in matches)

    def test_complete_index_shows_nested_keys(self, matcher):
        matches = matcher.find_matches("_['items'][0]")
        assert "_['items'][0]['name']" in matches
        assert "_['items'][0]['age']" in matches
        assert "_['items'][0]['city']" in matches
        assert "_['items'][0]['active']" in matches
        assert all(matcher._get_path_depth(m) == 3 for m in matches)

    def test_partial_key_fuzzy_match(self, matcher):
        matches = matcher.find_matches("_['ite")
        assert "_['items']" in matches
        assert all(matcher._get_path_depth(m) == 1 for m in matches)

    def test_out_of_bounds_index(self, matcher):
        matches = matcher.find_matches("_['items'][10]")
        assert len(matches) == 0

    def test_complete_path_shows_deeper_levels(self, matcher):
        matches = matcher.find_matches("_['metadata']")
        assert "_['metadata']['count']" in matches
        assert "_['metadata']['version']" in matches
        assert "_['metadata']['updated']" in matches
        assert all(matcher._get_path_depth(m) == 2 for m in matches)

    def test_partial_nested_key(self, matcher):
        matches = matcher.find_matches("_['items'][0]['n")
        assert "_['items'][0]['name']" in matches
        assert all(matcher._get_path_depth(m) == 3 for m in matches)
