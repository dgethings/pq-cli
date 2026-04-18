"""Test query evaluation performance."""

import time

import pytest

from pq.evaluator import evaluate_query


class TestPerformance:
    @pytest.fixture
    def test_queries(self):
        return [
            "_",
            "_['items']",
            "_['items'][0]",
            "_['items'][0]['name']",
            "_['metadata']",
            "_['metadata']['version']",
            "[item['name'] for item in _['items']]",
            "[item for item in _['items'] if item['age'] > 25]",
            "len(_['items'])",
            "_['items'][0]['name'] + ' test'",
        ]

    def test_all_queries_under_100ms(self, test_data, test_queries):
        for query in test_queries:
            start = time.perf_counter()
            evaluate_query(query, test_data)
            elapsed_ms = (time.perf_counter() - start) * 1000
            assert elapsed_ms < 100, f"Query '{query}' took {elapsed_ms:.2f}ms"

    def test_average_under_100ms(self, test_data, test_queries):
        total = 0
        for query in test_queries:
            start = time.perf_counter()
            evaluate_query(query, test_data)
            total += (time.perf_counter() - start) * 1000
        avg = total / len(test_queries)
        assert avg < 100, f"Average time {avg:.2f}ms exceeded 100ms"
