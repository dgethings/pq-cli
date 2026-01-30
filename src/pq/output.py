"""Output formatting and printing module."""

import json
import sys
from typing import Any


class OutputFormatter:
    """Format output for display and piping."""

    @staticmethod
    def format_output(result: Any) -> str:
        """Format result as JSON string.

        Args:
            result: Result to format

        Returns:
            Formatted JSON string
        """
        if result is None:
            return "null"
        elif isinstance(result, (str, int, float, bool)):
            return json.dumps(result)
        elif isinstance(result, (dict, list)):
            return json.dumps(result, indent=2, ensure_ascii=False)
        else:
            return str(result)

    @staticmethod
    def print_to_stdout(result: Any) -> None:
        """Print result to stdout for piping.

        Args:
            result: Result to print
        """
        output = OutputFormatter.format_output(result)
        sys.stdout.write(output)
        if not output.endswith("\n"):
            sys.stdout.write("\n")
        sys.stdout.flush()
