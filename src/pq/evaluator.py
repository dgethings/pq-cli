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


def evaluate_query(expression: str, data: dict[str, Any]) -> Any:
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
        raise QueryEvaluationError("Empty expression")

    restricted_globals = {
        "__builtins__": ALLOWED_BUILTINS,
        "data": data,
    }

    try:
        result = eval(expression, restricted_globals, {})
        return result
    except SyntaxError as e:
        raise QueryEvaluationError(f"Syntax error: {e.msg} at line {e.lineno}")
    except NameError as e:
        name = str(e).split("'")[1]
        raise QueryEvaluationError(
            f"Name '{name}' is not defined. Available: data, {', '.join(sorted(ALLOWED_BUILTINS.keys()))}"
        )
    except TypeError as e:
        raise QueryEvaluationError(f"Type error: {e}")
    except KeyError as e:
        raise QueryEvaluationError(f"Key error: {e}")
    except AttributeError as e:
        raise QueryEvaluationError(f"Attribute error: {e}")
    except ValueError as e:
        raise QueryEvaluationError(f"Value error: {e}")
    except IndexError as e:
        raise QueryEvaluationError(f"Index error: {e}")
    except Exception as e:
        raise QueryEvaluationError(f"Evaluation error: {e}")
