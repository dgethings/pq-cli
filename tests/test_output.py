"""Test output formatting."""

import json


from pq.output import OutputFormatter


class TestFormatOutput:
    def test_dict_output(self, test_data):
        result = OutputFormatter.format_output(test_data)
        parsed = json.loads(result)
        assert parsed == test_data

    def test_list_output(self, test_data):
        items = test_data["items"]
        result = OutputFormatter.format_output(items)
        parsed = json.loads(result)
        assert parsed == items

    def test_string_output(self, test_data):
        name = test_data["items"][0]["name"]
        result = OutputFormatter.format_output(name)
        assert json.loads(result) == name

    def test_integer_output(self, test_data):
        age = test_data["items"][0]["age"]
        result = OutputFormatter.format_output(age)
        assert json.loads(result) == age

    def test_float_output(self):
        result = OutputFormatter.format_output(3.14)
        assert json.loads(result) == 3.14

    def test_boolean_output(self, test_data):
        active = test_data["items"][0]["active"]
        result = OutputFormatter.format_output(active)
        assert json.loads(result) == active

    def test_none_output(self):
        result = OutputFormatter.format_output(None)
        assert result == "null"

    def test_list_comprehension_output(self, test_data):
        names = [item["name"] for item in test_data["items"]]
        result = OutputFormatter.format_output(names)
        parsed = json.loads(result)
        assert parsed == names

    def test_filtered_list_output(self, test_data):
        filtered = [item for item in test_data["items"] if item["age"] > 25]
        result = OutputFormatter.format_output(filtered)
        parsed = json.loads(result)
        assert parsed == filtered

    def test_unknown_type_output(self):
        result = OutputFormatter.format_output({1, 2, 3})
        assert "set" in result or "{" in result
