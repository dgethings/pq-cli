"""Test edge case handling."""

import json
from pathlib import Path

import pytest

from pq.evaluator import evaluate_query
from pq.loader import DocumentLoadError, load_document


class TestEmptyDocuments:
    def test_empty_json_object(self, tmp_path):
        file = tmp_path / "empty.json"
        file.write_text("{}")
        data = load_document(file_path=file)
        assert data == {}

    def test_empty_json_array(self, tmp_path):
        file = tmp_path / "array.json"
        file.write_text("[]")
        data = load_document(file_path=file)
        assert data == []
        result = evaluate_query("len(_)", data)
        assert result == 0


class TestMalformedDocuments:
    def test_malformed_json(self, tmp_path):
        file = tmp_path / "bad.json"
        file.write_text('{"invalid": json}')
        with pytest.raises(DocumentLoadError):
            load_document(file_path=file)


class TestNonExistentFile:
    def test_file_not_found(self):
        with pytest.raises(DocumentLoadError, match="File not found"):
            load_document(file_path=Path("/nonexistent/file.json"))


class TestSpecialCharacters:
    def test_json_with_special_characters(self, tmp_path):
        file = tmp_path / "special.json"
        file.write_text('{"key": "value with \\"quotes\\" and \\n newlines"}')
        data = load_document(file_path=file)
        assert "quotes" in data["key"]
        assert "\n" in data["key"]


class TestDeeplyNestedStructures:
    def test_deeply_nested_access(self, tmp_path):
        file = tmp_path / "nested.json"
        file.write_text('{"a": {"b": {"c": {"d": {"e": "value"}}}}}')
        data = load_document(file_path=file)
        result = evaluate_query("_['a']['b']['c']['d']['e']", data)
        assert result == "value"


class TestLargeDocuments:
    def test_large_list(self, tmp_path):
        large_data = {"items": [{"id": i, "value": "test"} for i in range(1000)]}
        file = tmp_path / "large.json"
        file.write_text(json.dumps(large_data))
        data = load_document(file_path=file)
        result = evaluate_query("len(_['items'])", data)
        assert result == 1000
