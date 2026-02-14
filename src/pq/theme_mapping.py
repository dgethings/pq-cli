"""Theme mapping module for syntax highlighting."""

from typing import Final


THEME_MAPPING: Final[dict[str, str]] = {
    "atom-one-dark": "one-dark",
    "atom-one-light": "pastie",
    "catppuccin-latte": "paraiso-light",
    "catppuccin-mocha": "paraiso-dark",
    "dracula": "dracula",
    "flexoki": "pastie",
    "gruvbox": "gruvbox-dark",
    "monokai": "monokai",
    "nord": "nord",
    "rose-pine": "pastie",
    "rose-pine-dawn": "paraiso-light",
    "rose-pine-moon": "paraiso-dark",
    "solarized-dark": "solarized-dark",
    "solarized-light": "solarized-light",
    "textual-ansi": "monokai",
    "textual-dark": "monokai",
    "textual-light": "pastie",
    "tokyo-night": "nord-darker",
}


def map_theme_to_pygments(textual_theme: str | None) -> str:
    """Map a Textual theme name to a compatible Pygments theme.

    Args:
        textual_theme: Textual theme name (e.g., "dracula", "monokai")

    Returns:
        Pygments theme name (e.g., "dracula", "monokai")
        Defaults to "monokai" for unknown or None themes
    """
    if textual_theme is None:
        return "monokai"

    return THEME_MAPPING.get(textual_theme, "monokai")
