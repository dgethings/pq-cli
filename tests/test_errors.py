"""Test enhanced error messages."""

import pytest

from pq.evaluator import QueryEvaluationError, evaluate_query


class TestErrorMessages:
    def test_empty_expression_raises(self, test_data):
        with pytest.raises(QueryEvaluationError, match="Please enter a query"):
            evaluate_query("", test_data)

    def test_missing_key_raises(self, test_data):
        with pytest.raises(QueryEvaluationError, match="not found"):
            evaluate_query("_['nonexistent_key']", test_data)

    def test_invalid_variable_raises(self, test_data):
        with pytest.raises(QueryEvaluationError, match="not available"):
            evaluate_query("invalid_var", test_data)

    def test_calling_non_function_raises(self, test_data):
        with pytest.raises(QueryEvaluationError):
            evaluate_query("_['items'][0]['name'](5)", test_data)

    def test_index_out_of_range_raises(self, test_data):
        with pytest.raises(QueryEvaluationError, match="Index out of range"):
            evaluate_query("_['items'][999]", test_data)

    def test_type_error_raises(self, test_data):
        with pytest.raises(QueryEvaluationError, match="Type mismatch"):
            evaluate_query("_['items'][0] + 'string'", test_data)

    def test_syntax_error_raises(self, test_data):
        with pytest.raises(QueryEvaluationError):
            evaluate_query("def foo():", test_data)

    def test_dunder_access_blocked(self, test_data):
        with pytest.raises(QueryEvaluationError, match="dunder"):
            evaluate_query("_.__class__", test_data)
