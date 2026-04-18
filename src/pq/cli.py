"""CLI argument parsing module."""

from __future__ import annotations

from pathlib import Path
import sys

import typer

from pq.config import load_config
from pq.evaluator import evaluate_query
from pq.loader import content_from_file, load_content
from pq.cli_arg import (
    Query,
    FilePath,
    FileTypeJSON,
    FileTypeYAML,
    FileTypeXML,
    FileTypeTOML,
    Theme,
    Version,
    consolidate_file_type_flags,
)
from pq.output import OutputFormatter
from pq.tui import QueryApp

__all__ = ["app"]

app = typer.Typer()


@app.command()
def main(
    query: Query,
    file_path: FilePath = None,
    file_type_json: FileTypeJSON = False,
    file_type_yaml: FileTypeYAML = False,
    file_type_xml: FileTypeXML = False,
    file_type_toml: FileTypeTOML = False,
    theme: Theme = None,
    v: Version = None,
) -> None:
    """Run a query against a document.

    Query a document using Python syntax.
    Reads from a file or stdin and evaluates the query against document data.
    """
    if query is None:
        raise typer.BadParameter("A query expression is required")

    file_type = consolidate_file_type_flags(
        file_type_json, file_type_yaml, file_type_xml, file_type_toml
    )

    query_path = Path(query)
    is_tui_mode = query_path.exists() and file_path is None

    if is_tui_mode:
        content, resolved_type = content_from_file(file_path=query_path)
        data = load_content(content=content, file_type=resolved_type, src=query)

        config = load_config()
        selected_theme = theme or config.theme

        tui = QueryApp(data=data, theme=selected_theme)
        tui.run()
        OutputFormatter.print_to_stdout(str(tui.query_string))
        raise typer.Exit(0)

    if file_path is not None:
        content, resolved_type = content_from_file(file_path=file_path)
        src = str(file_path)
    elif file_type is not None:
        content = sys.stdin.read()
        resolved_type = file_type
        src = "stdin"
    else:
        raise typer.BadParameter(
            "Must supply file path, or use a file type flag (-j/-y/-x/-t) when reading from stdin"
        )

    data = load_content(content=content, file_type=resolved_type, src=src)
    result = evaluate_query(query, data)
    OutputFormatter.print_to_stdout(result)


if __name__ == "__main__":
    app()
