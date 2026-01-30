"""CLI argument parsing module."""

import sys
from pathlib import Path
import typer

from pq.loader import DocumentLoadError, load_document, read_stdin


app = typer.Typer()


def main(
    file_path: str = typer.Argument(
        None,
        help="Path to JSON file to query",
    ),
) -> None:
    """Main CLI entry point.

    Args:
        file_path: Optional file path argument
    """
    try:
        if file_path:
            data = load_document(file_path=Path(file_path))
        else:
            if sys.stdin.isatty():
                typer.echo(
                    "Error: No input provided. Use: pq <file.json> or cat file.json | pq",
                    err=True,
                )
                raise typer.Exit(1)
            stdin_content = read_stdin()
            data = load_document(stdin_content=stdin_content)

        from pq.main import QueryApp

        QueryApp(data).run()

    except DocumentLoadError as e:
        typer.echo(f"Error loading document: {e}", err=True)
        raise typer.Exit(1)
    except KeyboardInterrupt:
        raise typer.Exit(0)
    except Exception as e:
        typer.echo(f"Unexpected error: {e}", err=True)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
