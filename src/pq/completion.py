"""Path completion and fuzzy matching module."""

import re
from typing import Any


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

    def _calculate_score(self, path: str, query: str) -> int:
        """Calculate fuzzy match score.

        Args:
            path: Path string to score
            query: Query string

        Returns:
            Score (higher is better)
        """
        if query in path:
            return len(query)

        parts = path.split("['")
        if len(parts) > 1:
            key_part = parts[-1].rstrip("']")
            if query in key_part.lower():
                return len(query) * 2

        return 0
