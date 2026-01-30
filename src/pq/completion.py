"""Path completion and fuzzy matching module."""

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
        self._extract_paths(self.data, "data")

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

    def find_matches(self, query: str, max_results: int = 10) -> list[str]:
        """Find paths that fuzzy match the query.

        Args:
            query: Query string to match
            max_results: Maximum number of results to return

        Returns:
            List of matching paths sorted by relevance
        """
        if not query:
            return self.paths[:max_results]

        query_lower = query.lower()
        matches = []

        for path in self.paths:
            score = self._calculate_score(path.lower(), query_lower)
            if score > 0:
                matches.append((path, score))

        matches.sort(key=lambda x: x[1], reverse=True)
        return [path for path, _ in matches[:max_results]]

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
