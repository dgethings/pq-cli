"""Test file type flag consolidation logic."""

import pytest
from pq.cli_arg import consolidate_file_type_flags
from pq.types import FileTypes


def test_no_flags():
    """Test with no file type flags set."""
    result = consolidate_file_type_flags(False, False, False, False)
    assert result is None


def test_single_json_flag():
    """Test with only JSON flag set."""
    result = consolidate_file_type_flags(True, False, False, False)
    assert result == FileTypes.json


def test_single_yaml_flag():
    """Test with only YAML flag set."""
    result = consolidate_file_type_flags(False, True, False, False)
    assert result == FileTypes.yaml


def test_single_xml_flag():
    """Test with only XML flag set."""
    result = consolidate_file_type_flags(False, False, True, False)
    assert result == FileTypes.xml


def test_single_toml_flag():
    """Test with only TOML flag set."""
    result = consolidate_file_type_flags(False, False, False, True)
    assert result == FileTypes.toml


def test_multiple_flags_raises_error():
    """Test that multiple flags raise an error."""
    with pytest.raises(Exception) as exc_info:
        consolidate_file_type_flags(True, True, False, False)
    assert "Only one file type flag may be specified" in str(exc_info.value)


def test_all_flags_raises_error():
    """Test that all flags set raises an error."""
    with pytest.raises(Exception) as exc_info:
        consolidate_file_type_flags(True, True, True, True)
    assert "Only one file type flag may be specified" in str(exc_info.value)


def test_json_and_yaml_flags_raises_error():
    """Test JSON and YAML flags together raise an error."""
    with pytest.raises(Exception) as exc_info:
        consolidate_file_type_flags(True, True, False, False)
    assert "Only one file type flag may be specified" in str(exc_info.value)


def test_xml_and_toml_flags_raises_error():
    """Test XML and TOML flags together raise an error."""
    with pytest.raises(Exception) as exc_info:
        consolidate_file_type_flags(False, False, True, True)
    assert "Only one file type flag may be specified" in str(exc_info.value)


def test_json_xml_toml_flags_raises_error():
    """Test JSON, XML, and TOML flags together raise an error."""
    with pytest.raises(Exception) as exc_info:
        consolidate_file_type_flags(True, False, True, True)
    assert "Only one file type flag may be specified" in str(exc_info.value)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
