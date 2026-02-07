"""Main Textual application module."""

from typing import Any, ClassVar, cast

from textual._path import CSSPathType
from textual.app import App, ComposeResult
from textual.binding import BindingType
from textual.containers import Horizontal
from textual.widgets import Footer, Header, Input, Static
from textual.widget import Widget

from pq.completion import FuzzyMatcher, PathExtractor
from pq.evaluator import QueryEvaluationError, evaluate_query
from pq.output import OutputFormatter


class QueryPrompt(Widget):
    """Input prompt for Python expressions."""

    def __init__(self, query: str) -> None:
        self.query_string: str = query
        super().__init__()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle Enter key press in the input field.

        Args:
            event: Input submitted event
        """
        event.stop()
        cast(QueryApp, self.app).action_accept_query()

    def compose(self) -> ComposeResult:
        # with Horizontal():
        #     yield Static("> ", id="prompt")
        yield Input(
            value=self.query_string,
            placeholder="Enter Python expression, use '_' to access data",
            id="query-input",
        )


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


class SuggestionBox(Static):
    """Display fuzzy path suggestions."""

    def update_suggestions(self, suggestions: list[str]) -> None:
        """Update the suggestions display.

        Args:
            suggestions: List of suggestion strings
        """
        if not suggestions:
            self.update("")
            self.remove_class("visible")
            return

        lines = "\n".join(f"  {s}" for s in suggestions[:10])
        self.update(f"[dim]Suggestions:[/dim]\n{lines}")
        self.add_class("visible")


class StatusBar(Static):
    """Display status and helpful hints."""

    def set_status(self, message: str) -> None:
        """Update the status message.

        Args:
            message: Status message to display
        """
        self.update(f"[dim]{message}[/dim]")


class QueryApp(App[None]):
    """Main Textual application for interactive Python querying."""

    CSS_PATH: ClassVar[CSSPathType | None] = "styles.tcss"
    TITLE: str | None = "pq - Interactive Python Query Tool"
    SUB_TITLE: str | None = "Type Python expressions to query your data"

    BINDINGS: ClassVar[list[BindingType]] = [
        ("ctrl+c", "quit", "Cancel & Quit"),
    ]

    def __init__(self, data: dict[str, Any]) -> None:
        """Initialize app with document data.

        Args:
            data: Document data to query
        """
        self.data = data
        self.final_result: Any = None

        path_extractor = PathExtractor(data)
        self.paths = path_extractor.get_paths()
        self.fuzzy_matcher = FuzzyMatcher(self.paths)
        self.query_string: str = "_"

        super().__init__()

    def compose(self) -> ComposeResult:
        """Compose the UI."""
        yield Header()
        yield QueryPrompt(query=self.query_string)
        yield SuggestionBox(id="suggestion-box")
        yield ResultDisplay(id="result-display")
        yield StatusBar(id="status-bar")
        yield Footer()

    def on_mount(self) -> None:
        """Set up the app on mount."""
        self.query_one("#query-input", Input).focus()
        status_bar = self.query_one("#status-bar", StatusBar)
        status_bar.set_status(
            "Type a Python expression to query the data. Press Enter to exit."
        )

    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle input changes for real-time evaluation.

        Args:
            event: Input changed event
        """
        query = event.value
        result_display = self.query_one("#result-display", ResultDisplay)
        suggestion_box = self.query_one("#suggestion-box", SuggestionBox)

        if not query.strip():
            result_display.update_result("")
            suggestion_box.update_suggestions([])
            self.final_result = None
            return

        suggestions = self.fuzzy_matcher.find_matches(query)
        suggestion_box.update_suggestions(suggestions)

        try:
            result = evaluate_query(query, self.data)
            result_display.update_result(result, is_error=False)
            self.query_string = query
            self.final_result = result
        except QueryEvaluationError as e:
            result_display.update_result(str(e), is_error=True)
            self.final_result = None

    def action_accept_query(self) -> None:
        """Accept the current query and exit."""
        self.exit(return_code=0)

    async def action_quit(self) -> None:
        """Quit without printing."""
        self.exit(return_code=130)
