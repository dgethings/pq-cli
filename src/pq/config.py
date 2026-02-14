"""Configuration file handling module."""

from pathlib import Path
import tomllib
from typing import NamedTuple


class Config(NamedTuple):
    """Application configuration."""

    theme: str | None


def load_config() -> Config:
    """Load configuration from file.

    Searches for config file in the following order:
    1. ./.pq.toml (current directory)
    2. $HOME/.config/pq/config.toml (XDG config dir)

    Returns:
        Config object with loaded settings, or None for missing values
    """
    config_paths = [
        Path(".pq.toml"),
        Path.home() / ".config" / "pq" / "config.toml",
    ]

    for config_path in config_paths:
        if config_path.exists():
            try:
                with open(config_path, "rb") as f:
                    data = tomllib.load(f)

                theme = data.get("theme", {}).get("name")
                return Config(theme=theme)
            except (tomllib.TOMLDecodeError, OSError, KeyError):
                continue

    return Config(theme=None)
