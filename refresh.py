"""Refresh script for anime_library_scanner_plugin."""

import sys
from pathlib import Path

PROJECT_ROOT = Path.cwd()
sys.path.insert(0, str(PROJECT_ROOT))

from plugins.anime_library_scanner_plugin.anime_library_scanner_plugin_cli import (
    register_cli,
)


def refresh() -> None:
    """Register CLI commands for anime_library_scanner_plugin."""
    register_cli()


if __name__ == "__main__":
    refresh()
