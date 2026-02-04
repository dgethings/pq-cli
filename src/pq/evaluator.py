"""Query evaluation module."""

from typing import Any


ALLOWED_BUILTINS = {
    "len": len,
    "sum": sum,
    "min": min,
    "max": max,
    "sorted": sorted,
    "filter": filter,
    "map": map,
    "list": list,
    "dict": dict,
    "set": set,
    "tuple": tuple,
    "str": str,
    "int": int,
    "float": float,
    "bool": bool,
    "type": type,
    "isinstance": isinstance,
    "range": range,
    "zip": zip,
    "enumerate": enumerate,
    "any": any,
    "all": all,
    "abs": abs,
    "round": round,
    "slice": slice,
}


class QueryEvaluationError(Exception):
    """Raised when query evaluation fails."""


def evaluate_query(expression: str, data: dict[str, Any]) -> dict[str, Any]:
    """Safely evaluate a Python expression with data context.

    Args:
        expression: Python expression to evaluate
        data: Document data available as 'data' variable

    Returns:
        Result of the expression evaluation

    Raises:
        QueryEvaluationError: If expression is invalid or evaluation fails
    """
    if not expression.strip():
        raise QueryEvaluationError(
            "Please enter a query. Try: _, _['key'], or _['items'][0]"
        )

    restricted_globals = {
        "__builtins__": ALLOWED_BUILTINS,
        "_": data,
    }

    try:
        return eval(expression, restricted_globals, {})
    except SyntaxError as e:
        raise QueryEvaluationError(
            f"Invalid Python syntax: {e.msg} at position {e.offset}. Check for missing quotes, brackets, or operators."
        )
    except NameError as e:
        name = str(e).split("'")[1]
        available = ", ".join(sorted(ALLOWED_BUILTINS.keys()))
        raise QueryEvaluationError(
            f"'{name}' is not available. Use '_' to access the document. Available functions: {available}, ..."
        )
    except TypeError as e:
        error_msg = str(e)
        if "subscriptable" in error_msg:
            raise QueryEvaluationError(
                "Cannot use brackets on this type. Make sure you're accessing a dictionary or list, not a string or number."
            )
        elif "not iterable" in error_msg:
            raise QueryEvaluationError(
                "This value cannot be iterated over. Use it directly or check if it's a list or dict first."
            )
        else:
            raise QueryEvaluationError(f"Type mismatch: {error_msg}")
    except KeyError as e:
        key = str(e).strip("'\"")
        raise QueryEvaluationError(
            f"Key '{key}' not found. Check the document structure or use fuzzy matching to find available keys."
        )
    except AttributeError as e:
        raise QueryEvaluationError(
            f"Invalid attribute access: {e}. Use dictionary-style access with brackets: data['key']"
        )
    except ValueError as e:
        raise QueryEvaluationError(f"Invalid value: {e}")
    except IndexError:
        raise QueryEvaluationError(
            "Index out of range. The list is shorter than the index you're trying to access."
        )
    except Exception as e:
        raise QueryEvaluationError(f"Query evaluation failed: {e}")
