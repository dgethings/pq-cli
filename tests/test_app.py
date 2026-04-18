"""Test QueryApp logic without TUI."""

from collections import Counter, defaultdict


from pq.evaluator import evaluate_query


class TestSimpleQueries:
    def test_simple_key_access(self, test_data):
        result = evaluate_query("_['items'][0]['name']", test_data)
        assert result == test_data["items"][0]["name"]

    def test_list_comprehension(self, test_data):
        result = evaluate_query("[item['name'] for item in _['items']]", test_data)
        assert result == [item["name"] for item in test_data["items"]]

    def test_filtered_list(self, test_data):
        result = evaluate_query(
            "[item for item in _['items'] if item['age'] > 25]", test_data
        )
        assert all(item["age"] > 25 for item in result)

    def test_metadata_access(self, test_data):
        result = evaluate_query("_['metadata']['version']", test_data)
        assert result == test_data["metadata"]["version"]


class TestCounterQueries:
    def test_counter_cities(self, test_data):
        result = evaluate_query(
            "Counter(item['city'] for item in _['items'])", test_data
        )
        assert isinstance(result, Counter)
        assert result["NYC"] == 2

    def test_counter_ages(self, test_data):
        result = evaluate_query("Counter([x['age'] for x in _['items']])", test_data)
        assert isinstance(result, Counter)
        assert result[30] == 1
        assert result[25] == 1
        assert result[35] == 1


class TestNamedTupleQueries:
    def test_namedtuple_creation(self, test_data):
        result = evaluate_query(
            "namedtuple('Person', 'name age')(_['items'][0]['name'], _['items'][0]['age'])",
            test_data,
        )
        assert result.name == test_data["items"][0]["name"]
        assert result.age == test_data["items"][0]["age"]


class TestDefaultdictQueries:
    def test_defaultdict_creation(self, test_data):
        result = evaluate_query("defaultdict(list, {'a': [1, 2]})", test_data)
        assert isinstance(result, defaultdict)
        assert result["a"] == [1, 2]
