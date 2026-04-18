"""Test 2GB file size limit."""

from pathlib import Path

import pytest

from pq.loader import DocumentLoadError, MAX_FILE_SIZE, load_document


def test_max_file_size_constant():
    assert MAX_FILE_SIZE == 2 * 1024 * 1024 * 1024


class TestFileSizeLimits:
    def test_small_file_loads(self, tmp_path):
        file = tmp_path / "small.json"
        file.write_text('{"test": "value"}')
        data = load_document(file_path=file)
        assert data == {"test": "value"}

    def test_nonexistent_file_raises(self):
        with pytest.raises(DocumentLoadError, match="File not found"):
            load_document(file_path=Path("nonexistent_file.json"))
