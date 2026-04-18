"""Query evaluation module."""

from __future__ import annotations

import ast
from collections import Counter, defaultdict, OrderedDict, deque, namedtuple
from typing import Any

__all__ = [
    "ALLOWED_BUILTINS",
    "QueryEvaluationError",
    "evaluate_query",
]


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
    "Counter": Counter,
    "defaultdict": defaultdict,
    "OrderedDict": OrderedDict,
    "deque": deque,
    "namedtuple": namedtuple,
}

_SAFE_NODE_TYPES = frozenset(
    {
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.BoolOp,
        ast.Compare,
        ast.Call,
        ast.IfExp,
        ast.Attribute,
        ast.Subscript,
        ast.Starred,
        ast.Name,
        ast.Constant,
        ast.List,
        ast.Tuple,
        ast.Set,
        ast.Dict,
        ast.ListComp,
        ast.SetComp,
        ast.DictComp,
        ast.GeneratorExp,
        ast.comprehension,
        ast.Slice,
        ast.Index,
        ast.Load,
        ast.Store,
        ast.Del,
        ast.keyword,
        ast.Lambda,
        ast.arguments,
        ast.arg,
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.FloorDiv,
        ast.Mod,
        ast.Pow,
        ast.LShift,
        ast.RShift,
        ast.BitOr,
        ast.BitXor,
        ast.BitAnd,
        ast.MatMult,
        ast.UAdd,
        ast.USub,
        ast.Not,
        ast.Invert,
        ast.And,
        ast.Or,
        ast.Eq,
        ast.NotEq,
        ast.Lt,
        ast.LtE,
        ast.Gt,
        ast.GtE,
        ast.Is,
        ast.IsNot,
        ast.In,
        ast.NotIn,
    }
)

_ALLOWED_BIN_OPS = frozenset(
    {
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.FloorDiv,
        ast.Mod,
        ast.Pow,
        ast.LShift,
        ast.RShift,
        ast.BitOr,
        ast.BitXor,
        ast.BitAnd,
        ast.MatMult,
    }
)

_ALLOWED_UNARY_OPS = frozenset({ast.UAdd, ast.USub, ast.Not, ast.Invert})

_ALLOWED_CMP_OPS = frozenset(
    {
        ast.Eq,
        ast.NotEq,
        ast.Lt,
        ast.LtE,
        ast.Gt,
        ast.GtE,
        ast.Is,
        ast.IsNot,
        ast.In,
        ast.NotIn,
    }
)


class QueryEvaluationError(Exception):
    """Raised when query evaluation fails."""


def _validate_ast(node: ast.AST) -> None:
    """Walk the AST and reject dangerous node types.

    Args:
        node: AST node to validate

    Raises:
        QueryEvaluationError: If the expression contains unsafe constructs
    """
    for child in ast.walk(node):
        child_type = type(child)

        if child_type not in _SAFE_NODE_TYPES:
            raise QueryEvaluationError(
                f"Operation '{child_type.__name__}' is not allowed for safety reasons."
            )

        if isinstance(child, ast.BinOp):
            if type(child.op) not in _ALLOWED_BIN_OPS:
                raise QueryEvaluationError(
                    f"Operator '{type(child.op).__name__}' is not allowed."
                )

        if isinstance(child, ast.UnaryOp):
            if type(child.op) not in _ALLOWED_UNARY_OPS:
                raise QueryEvaluationError(
                    f"Operator '{type(child.op).__name__}' is not allowed."
                )

        if isinstance(child, ast.BoolOp):
            if child.op not in (ast.And, ast.Or):
                raise QueryEvaluationError(
                    f"Boolean operator '{type(child.op).__name__}' is not allowed."
                )

        if isinstance(child, ast.Compare):
            for op in child.ops:
                if type(op) not in _ALLOWED_CMP_OPS:
                    raise QueryEvaluationError(
                        f"Comparison operator '{type(op).__name__}' is not allowed."
                    )

        if isinstance(child, ast.Name) and child.id.startswith("__"):
            raise QueryEvaluationError(
                "Double-underscore (dunder) access is not allowed for safety reasons."
            )

        if isinstance(child, ast.Attribute) and child.attr.startswith("__"):
            raise QueryEvaluationError(
                "Double-underscore (dunder) attribute access is not allowed for safety reasons."
            )


def evaluate_query(expression: str, data: Any) -> Any:
    """Safely evaluate a Python expression with data context.

    Args:
        expression: Python expression to evaluate
        data: Document data available as '_' variable

    Returns:
        Result of the expression evaluation

    Raises:
        QueryEvaluationError: If expression is invalid or evaluation fails
    """
    if not expression.strip():
        raise QueryEvaluationError(
            "Please enter a query. Try: _, _['key'], or _['items'][0]"
        )

    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as e:
        raise QueryEvaluationError(
            f"Invalid Python syntax: {e.msg} at position {e.offset}. Check for missing quotes, brackets, or operators."
        )

    _validate_ast(tree)

    restricted_globals = {
        "__builtins__": ALLOWED_BUILTINS,
        "_": data,
    }

    try:
        return eval(expression, restricted_globals, {"__builtins__": {}})
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
            f"Invalid attribute access: {e}. Use bracket-style access: _['key']"
        )
    except ValueError as e:
        raise QueryEvaluationError(f"Invalid value: {e}")
    except IndexError:
        raise QueryEvaluationError(
            "Index out of range. The list is shorter than the index you're trying to access."
        )
    except Exception as e:
        raise QueryEvaluationError(f"Query evaluation failed: {e}")
