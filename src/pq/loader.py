"""Document loading and validation module."""

from pathlib import Path
from typing import Any
import json
import sys


MAX_FILE_SIZE = 2 * 1024 * 1024 * 1024


class DocumentLoadError(Exception):
    """Raised when document loading fails."""


def load_document(
    file_path: Path | None = None, stdin_content: str | None = None
) -> dict[str, Any]:
    """Load a document from file path or stdin.

    Args:
        file_path: Path to the file to load
        stdin_content: Content from stdin if available

    Returns:
        Parsed document as a dictionary

    Raises:
        DocumentLoadError: If file loading or parsing fails
    """
    if file_path:
        return _load_from_file(file_path)
    elif stdin_content:
        return _load_from_string(stdin_content)
    else:
        raise DocumentLoadError("No file path or stdin content provided")


def _load_from_file(file_path: Path) -> dict[str, Any]:
    """Load document from file path."""
    if not file_path.exists():
        raise DocumentLoadError(f"File not found: {file_path}")

    file_size = file_path.stat().st_size
    if file_size > MAX_FILE_SIZE:
        raise DocumentLoadError(
            f"File too large ({file_size / (1024 * 1024 * 1024):.2f}GB). "
            f"Maximum size is {MAX_FILE_SIZE / (1024 * 1024 * 1024):.0f}GB"
        )

    try:
        content = file_path.read_text(encoding="utf-8")
        return _parse_json(content, str(file_path))
    except UnicodeDecodeError:
        raise DocumentLoadError(f"File encoding error: {file_path}")
    except OSError as e:
        raise DocumentLoadError(f"Failed to read file: {e}")


def _load_from_string(content: str) -> dict[str, Any]:
    """Load document from string (stdin)."""
    return _parse_json(content, "stdin")


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
        if not isinstance(data, dict):
            raise DocumentLoadError(
                f"Document must be a JSON object (dict), got {type(data).__name__}"
            )
        return data
    except json.JSONDecodeError as e:
        raise DocumentLoadError(
            f"Invalid JSON in {source}: {e.msg} at line {e.lineno}, column {e.colno}"
        )


def read_stdin() -> str:
    """Read content from stdin.

    Returns:
        Content from stdin as string
    """
    return sys.stdin.read()
