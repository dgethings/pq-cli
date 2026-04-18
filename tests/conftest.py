"""Shared test fixtures for pq-cli."""

from pathlib import Path

import pytest

from pq.loader import load_document


@pytest.fixture
def test_data():
    """Load test data from test_data.json."""
    return load_document(file_path=Path(__file__).parent / "test_data.json")


@pytest.fixture
def test_data_path():
    """Return path to test_data.json."""
    return Path(__file__).parent / "test_data.json"
