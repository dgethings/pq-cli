"""Document loading and validation module."""

from pathlib import Path
from typing import Any
from xml.parsers import expat
import json
import tomllib

import xmltodict
import yaml

from pq.types import FileTypes


MAX_FILE_SIZE = 2 * 1024 * 1024 * 1024


class DocumentLoadError(Exception):
    """Raised when document loading fails."""


def load_document(file_path: Path) -> dict[str, Any]:
    """Load document from file path.

    Args:
        file_path: Path to the file to load

    Returns:
        Parsed document as dictionary

    Raises:
        DocumentLoadError: If file loading fails
    """
    content, file_type = content_from_file(file_path)
    return load_content(content, file_type, str(file_path))


def content_from_file(file_path: Path) -> tuple[str, FileTypes]:
    """Load document from file path."""
    if not file_path.exists():
        raise DocumentLoadError(f"File not found: {file_path}")

    file_size = file_path.stat().st_size
    if file_size > MAX_FILE_SIZE:
        raise DocumentLoadError(
            f"File too large ({file_size / (1024 * 1024 * 1024):.2f}GB). Maximum size is {MAX_FILE_SIZE / (1024 * 1024 * 1024):.0f}GB"
        )

    ft = FileTypes(file_path.suffix.lstrip("."))
    return file_path.read_text(encoding="utf-8"), ft


def load_content(content: str, file_type: FileTypes, src: str) -> dict[str, Any]:
    """Load content using parser based on file type."""
    match file_type:
        case "json":
            return _parse_json(content, src)
        case "yaml":
            return _parse_yaml(content, src)
        case "xml":
            return _parse_xml(content, src)
        case "toml":
            return _parse_toml(content, src)
        case _:
            raise RuntimeError(f"{file_type} currently not supported")


def _validate_dict(data: Any, format_name: str) -> dict[str, Any]:
    """Validate that parsed data is a dictionary.

    Args:
        data: Parsed data to validate
        format_name: Name of the format for error messages

    Returns:
        The validated data

    Raises:
        DocumentLoadError: If data is not a dict
    """
    if not isinstance(data, dict):
        raise DocumentLoadError(
            f"Document must be a {format_name} object (dict), got {type(data).__name__}"
        )
    return data


def _parse_json(content: str, source: str) -> dict[str, Any]:
    """Parse JSON content.

    Args:
        content: JSON string to parse
        source: Source description for error messages

    Returns:
        Parsed JSON as dictionary

    Raises:
        DocumentLoadError: If JSON is invalid
    """
    try:
        data = json.loads(content)
        return _validate_dict(data, "JSON")
    except json.JSONDecodeError as e:
        raise DocumentLoadError(
            f"Invalid JSON in {source}: {e.msg} at line {e.lineno}, column {e.colno}"
        )


def _parse_yaml(content: str, source: str) -> dict[str, Any]:
    """Parse YAML content.

    Args:
        content: YAML string to parse
        source: Source description for error messages

    Returns:
        Parsed YAML as dictionary

    Raises:
        DocumentLoadError: If YAML is invalid
    """
    try:
        data = yaml.safe_load(content)
        return _validate_dict(data, "YAML")
    except yaml.YAMLError as e:
        raise DocumentLoadError(f"Invalid YAML in {source}: {e}")


def _parse_xml(content: str, source: str) -> dict[str, Any]:
    """Parse XML content.

    Args:
        content: XML string to parse
        source: Source description for error messages

    Returns:
        Parsed XML as dictionary

    Raises:
        DocumentLoadError: If XML is invalid
    """
    try:
        data = xmltodict.parse(content)
        return _validate_dict(data, "XML")
    except expat.ExpatError as e:
        raise DocumentLoadError(f"Invalid XML in {source}: {e}")
    except Exception as e:
        raise DocumentLoadError(f"Failed to parse XML from {source}: {e}")


def _parse_toml(content: str, source: str) -> dict[str, Any]:
    """Parse TOML content.

    Args:
        content: TOML string to parse
        source: Source description for error messages

    Returns:
        Parsed TOML as dictionary

    Raises:
        DocumentLoadError: If TOML is invalid
    """
    try:
        return tomllib.loads(content)
    except tomllib.TOMLDecodeError as e:
        raise DocumentLoadError(f"Invalid TOML in {source}: {e}")
