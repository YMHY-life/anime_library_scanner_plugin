"""anime_library_scanner_plugin - Anime filename parser and library scanner.

Integrates with external_media_manager to parse anime metadata from filenames.
"""

import os
import sys

project_root = os.getcwd()
sys.path.insert(0, project_root)

from plugins.anime_library_scanner_plugin.anime_library_scanner_plugin import (
    AnimeLibraryScannerPlugin,
    is_anitopy_available,
)
from plugins.anime_library_scanner_plugin.models import ParsedAnimeFile
from plugins.anime_library_scanner_plugin.anime_library_scanner_plugin_cli import (
    register_cli,
)

__all__ = [
    "AnimeLibraryScannerPlugin",
    "ParsedAnimeFile",
    "is_anitopy_available",
    "register_cli",
]
