"""Path completion and fuzzy matching module."""

from __future__ import annotations

import re
from typing import Any

__all__ = ["PathExtractor", "FuzzyMatcher"]


class PathExtractor:
    """Extract valid paths from document structure."""

    def __init__(self, data: dict[str, Any]) -> None:
        """Initialize with document data.

        Args:
            data: Document data to extract paths from
        """
        self.data = data
        self.paths: list[str] = []
        self._extract_paths(self.data, "_")

    def _extract_paths(self, obj: Any, current_path: str) -> None:
        """Recursively extract paths from object.

        Args:
            obj: Object to extract paths from
            current_path: Current path prefix
        """
        if isinstance(obj, dict):
            for key, value in obj.items():
                new_path = f"{current_path}['{key}']"
                self.paths.append(new_path)
                self._extract_paths(value, new_path)
        elif isinstance(obj, (list, tuple)):
            for i, value in enumerate(obj):
                new_path = f"{current_path}[{i}]"
                self.paths.append(new_path)
                self._extract_paths(value, new_path)

    def get_paths(self) -> list[str]:
        """Get all extracted paths.

        Returns:
            List of path strings
        """
        return self.paths


class FuzzyMatcher:
    """Fuzzy matching for path suggestions."""

    def __init__(self, paths: list[str]) -> None:
        """Initialize with paths.

        Args:
            paths: List of path strings to match against
        """
        self.paths = paths

    def _get_path_depth(self, path: str) -> int:
        """Calculate depth of bracket access in path.

        Args:
            path: Path string to analyze

        Returns:
            Number of bracket access levels
        """
        complete_brackets = re.findall(r"\[[^\]]+\]", path)
        return len(complete_brackets)

    def _matches_prefix(self, path: str, query: str) -> bool:
        """Check if path matches query prefix.

        Handles partial keys with fuzzy matching.

        Args:
            path: Full path string
            query: Query prefix (may be partial)

        Returns:
            True if path matches query prefix
        """
        if not query or query == "_":
            return path.startswith("_")

        if path.startswith(query):
            return True

        path_lower = path.lower()

        bracket_match = re.search(r"\['([^']*)$", query)
        if bracket_match:
            partial_key = bracket_match.group(1)
            base_prefix = query[: bracket_match.start()]
            if path_lower.startswith(base_prefix.lower()):
                key_match = re.search(r"\['([^']+)'\]", path[len(base_prefix) :])
                if key_match:
                    actual_key = key_match.group(1)
                    return partial_key.lower() in actual_key.lower()

        return False

    def _has_partial_key(self, query: str) -> bool:
        """Check if query ends with a partial key.

        Args:
            query: Query string to check

        Returns:
            True if query ends with a partial key
        """
        return bool(re.search(r"\['([^']*)$", query))

    def _filter_to_next_level(self, paths: list[str], query: str) -> list[str]:
        """Filter paths to only show next-level suggestions.

        Args:
            paths: List of all available paths
            query: Current query string

        Returns:
            List of paths at the next level only
        """
        query_depth = self._get_path_depth(query)
        target_depth = query_depth + 1

        matched = []
        for path in paths:
            if not self._matches_prefix(path, query):
                continue

            path_depth = self._get_path_depth(path)
            if path_depth == target_depth:
                matched.append(path)

        return matched

    def find_matches(self, query: str, max_results: int = 10) -> list[str]:
        """Find paths that fuzzy match the query.

        Args:
            query: Query string to match
            max_results: Maximum number of results to return

        Returns:
            List of matching paths sorted by relevance
        """
        if not query or query == "_":
            return self._filter_to_next_level(self.paths, "_")

        return self._filter_to_next_level(self.paths, query)[:max_results]

    def get_keys_at_path(self, base_path: str) -> list[str]:
        """Get available keys at a given path.

        Args:
            base_path: The path to get keys for (e.g., "_" or "_['items']")

        Returns:
            List of available keys (string keys or integer indices)
        """
        keys: set[str] = set()

        for path in self.paths:
            if not path.startswith(base_path):
                continue

            remaining = path[len(base_path) :]
            if not remaining.startswith("[") or len(remaining) < 2:
                continue

            bracket_content = remaining[1:].split("]")[0]

            if bracket_content.startswith("'"):
                keys.add(bracket_content.strip("'"))
            elif bracket_content.startswith('"'):
                keys.add(bracket_content.strip('"'))
            elif bracket_content.isdigit():
                keys.add(bracket_content)

        return sorted(
            keys, key=lambda x: (not x.isdigit(), int(x) if x.isdigit() else x)
        )

    def get_common_prefix(self, keys: list[str]) -> str:
        """Get longest common prefix of a list of keys.

        Args:
            keys: List of keys to find common prefix of

        Returns:
            Longest common prefix string
        """
        if not keys:
            return ""
        if len(keys) == 1:
            return keys[0]

        first = keys[0]
        for i, char in enumerate(first):
            for key in keys[1:]:
                if i >= len(key) or key[i] != char:
                    return first[:i]
        return first

    def find_keys_at_path(self, base_path: str, prefix: str) -> list[str]:
        """Find keys at a given path that match a prefix.

        Args:
            base_path: The path to get keys for
            prefix: Prefix to filter keys

        Returns:
            List of matching keys
        """
        all_keys = self.get_keys_at_path(base_path)
        if not prefix:
            return all_keys

        prefix_lower = prefix.lower()
        return [k for k in all_keys if k.lower().startswith(prefix_lower)]
