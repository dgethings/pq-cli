"""Test suggestions integration."""

import pytest

from pq.completion import FuzzyMatcher, PathExtractor
from pq.evaluator import evaluate_query


@pytest.fixture
def fuzzy_matcher(test_data):
    """Create FuzzyMatcher from test data."""
    extractor = PathExtractor(test_data)
    return FuzzyMatcher(extractor.get_paths())


class TestSuggestionsIntegration:
    def test_partial_key_name(self, fuzzy_matcher):
        suggestions = fuzzy_matcher.find_matches("_['items'][0]['n")
        assert len(suggestions) > 0
        assert "_['items'][0]['name']" in suggestions

    def test_partial_key_age(self, fuzzy_matcher):
        suggestions = fuzzy_matcher.find_matches("_['items'][0]['a")
        assert len(suggestions) > 0
        assert "_['items'][0]['age']" in suggestions

    def test_partial_metadata_key(self, fuzzy_matcher):
        suggestions = fuzzy_matcher.find_matches("_['metadata']['v")
        assert len(suggestions) > 0
        assert "_['metadata']['version']" in suggestions

    def test_empty_query(self, fuzzy_matcher):
        suggestions = fuzzy_matcher.find_matches("")
        assert len(suggestions) > 0

    def test_evaluation_with_suggestions(self, test_data, fuzzy_matcher):
        suggestions = fuzzy_matcher.find_matches("_['items'][0]")
        assert len(suggestions) > 0
        result = evaluate_query("_['items'][0]['name']", test_data)
        assert result == test_data["items"][0]["name"]
