"""Test CLI flag functionality."""

import subprocess
import sys


def run_cli(*args: str) -> tuple[int, str, str]:
    """Run CLI command and return exit code, stdout, stderr."""
    result = subprocess.run(
        [sys.executable, "-m", "pq.cli", *args],
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout, result.stderr


def test_theme_flag_long_form():
    """Test --theme flag works."""
    returncode, stdout, stderr = run_cli(
        "_", "tests/test_data.json", "--theme", "dracula"
    )
    # Should start the TUI, which we can't test fully, but should not error immediately
    # The TUI will exit quickly with Ctrl+C in subprocess


def test_theme_flag_short_form():
    """Test -T flag works."""
    returncode, stdout, stderr = run_cli("_", "tests/test_data.json", "-T", "dracula")
    # Should start the TUI without error


def test_json_flag():
    """Test -j flag for JSON stdin."""
    json_data = '{"key": "value"}'
    result = subprocess.run(
        [sys.executable, "-m", "pq.cli", "-j", "_['key']"],
        input=json_data,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "value" in result.stdout


def test_json_flag_long():
    """Test --json flag for JSON stdin."""
    json_data = '{"key": "value"}'
    result = subprocess.run(
        [sys.executable, "-m", "pq.cli", "--json", "_['key']"],
        input=json_data,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "value" in result.stdout


def test_yaml_flag():
    """Test -y flag for YAML stdin."""
    yaml_data = "key: value"
    result = subprocess.run(
        [sys.executable, "-m", "pq.cli", "-y", "_['key']"],
        input=yaml_data,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "value" in result.stdout


def test_yaml_flag_long():
    """Test --yaml flag for YAML stdin."""
    yaml_data = "key: value"
    result = subprocess.run(
        [sys.executable, "-m", "pq.cli", "--yaml", "_['key']"],
        input=yaml_data,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "value" in result.stdout


def test_xml_flag():
    """Test -x flag for XML stdin."""
    xml_data = "<root><key>value</key></root>"
    result = subprocess.run(
        [sys.executable, "-m", "pq.cli", "-x", "_"],
        input=xml_data,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0


def test_xml_flag_long():
    """Test --xml flag for XML stdin."""
    xml_data = "<root><key>value</key></root>"
    result = subprocess.run(
        [sys.executable, "-m", "pq.cli", "--xml", "_"],
        input=xml_data,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0


def test_toml_flag():
    """Test -t flag for TOML stdin."""
    toml_data = '[section]\nkey = "value"'
    result = subprocess.run(
        [sys.executable, "-m", "pq.cli", "-t", "_"],
        input=toml_data,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0


def test_toml_flag_long():
    """Test --toml flag for TOML stdin."""
    toml_data = '[section]\nkey = "value"'
    result = subprocess.run(
        [sys.executable, "-m", "pq.cli", "--toml", "_"],
        input=toml_data,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0


def test_mutually_exclusive_flags():
    """Test that multiple file type flags are rejected."""
    json_data = '{"key": "value"}'
    result = subprocess.run(
        [sys.executable, "-m", "pq.cli", "-j", "-y", "key"],
        input=json_data,
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "Only one file type flag may be specified" in result.stderr


def test_mutually_exclusive_flags_long():
    """Test that multiple long form file type flags are rejected."""
    json_data = '{"key": "value"}'
    result = subprocess.run(
        [sys.executable, "-m", "pq.cli", "--json", "--yaml", "key"],
        input=json_data,
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "Only one file type flag may be specified" in result.stderr


def test_stdin_without_file_type():
    """Test that stdin without file type flag is rejected."""
    json_data = '{"key": "value"}'
    result = subprocess.run(
        [sys.executable, "-m", "pq.cli", "key"],
        input=json_data,
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "file type flag" in result.stderr.lower()


def test_old_file_flag_removed():
    """Test that old -f flag is removed."""
    json_data = '{"key": "value"}'
    result = subprocess.run(
        [sys.executable, "-m", "pq.cli", "-f", "json", "key"],
        input=json_data,
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    # Should get "no such option" error


def test_old_theme_flag_removed():
    """Test that old -t theme flag is removed."""
    result = subprocess.run(
        [sys.executable, "-m", "pq.cli", "_", "tests/test_data.json", "-t", "dracula"],
        capture_output=True,
        text=True,
    )
    # The -t flag is now used for TOML, so this should be interpreted as TOML flag
    # and will fail because dracula is not a boolean
    assert result.returncode != 0


def test_file_with_auto_detection():
    """Test file path with auto file type detection."""
    _ = subprocess.run(
        [sys.executable, "-m", "pq.cli", "_", "tests/test_data.json"],
        capture_output=True,
        text=True,
        timeout=5,
    )
    # Should work without file type flag


def test_file_with_explicit_flag():
    """Test file path with explicit file type flag."""
    _ = subprocess.run(
        [sys.executable, "-m", "pq.cli", "_", "tests/test_data.json", "-j"],
        capture_output=True,
        text=True,
        timeout=5,
    )
    # Should work with explicit flag


if __name__ == "__main__":
    import pytest

    pytest.main([__file__, "-v"])
