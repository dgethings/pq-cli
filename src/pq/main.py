"""Main Textual application module."""

from typing import Any

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Footer, Header, Input, Static
from textual.widget import Widget

from pq.evaluator import QueryEvaluationError, evaluate_query
from pq.output import OutputFormatter


class QueryPrompt(Widget):
    """Input prompt for Python expressions."""

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Static("> ", id="prompt")
            yield Input(placeholder="Enter Python expression", id="query-input")


class ResultDisplay(Static):
    """Display query results or errors."""

    def update_result(self, result: Any, is_error: bool = False) -> None:
        """Update the display with new result.

        Args:
            result: Result to display
            is_error: Whether this is an error message
        """
        if is_error:
            self.update(f"[error]{result}[/error]")
        else:
            formatted = OutputFormatter.format_output(result)
            self.update(formatted)


class QueryApp(App[None]):
    """Main Textual application for interactive Python querying."""

    CSS_PATH = "styles.tcss"

    BINDINGS = [
        ("enter", "accept_query", "Accept query"),
        ("ctrl+c", "quit", "Quit"),
    ]

    def __init__(self, data: dict[str, Any]) -> None:
        """Initialize app with document data.

        Args:
            data: Document data to query
        """
        self.data = data
        self.final_result: Any = None
        super().__init__()

    def compose(self) -> ComposeResult:
        """Compose the UI."""
        yield Header()
        yield QueryPrompt()
        yield ResultDisplay(id="result-display")
        yield Footer()

    def on_mount(self) -> None:
        """Set up the app on mount."""
        self.query_one("#query-input", Input).focus()

    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle input changes for real-time evaluation.

        Args:
            event: Input changed event
        """
        query = event.value
        result_display = self.query_one("#result-display", ResultDisplay)

        if not query.strip():
            result_display.update_result("")
            self.final_result = None
            return

        try:
            result = evaluate_query(query, self.data)
            result_display.update_result(result, is_error=False)
            self.final_result = result
        except QueryEvaluationError as e:
            result_display.update_result(str(e), is_error=True)
            self.final_result = None

    def action_accept_query(self) -> None:
        """Accept the current query and exit."""
        if self.final_result is not None:
            OutputFormatter.print_to_stdout(self.final_result)
        self.exit(self.final_result)
