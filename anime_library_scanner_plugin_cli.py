"""CLI commands and registration for anime_library_scanner_plugin."""

from __future__ import annotations

import argparse
import sys

from managers.cli_manager import CLIManager, ModuleRegistration, Command, CommandArg


# ─────────────────────────────────────────────────────────────────────────────
# Handler Functions
# ─────────────────────────────────────────────────────────────────────────────


def parse_filename(args: argparse.Namespace) -> int:
    """Parse an anime filename and display extracted metadata."""
    from plugins.anime_library_scanner_plugin.anime_library_scanner_plugin import (
        AnimeLibraryScannerPlugin,
        is_anitopy_available,
    )

    if not is_anitopy_available():
        print("Error: anitopy not installed.", file=sys.stderr)
        print("Install with: pip install anitopy>=2.1.1", file=sys.stderr)
        return 1

    plugin = AnimeLibraryScannerPlugin()
    result = plugin.parse_filename(args.filename)

    if result is None:
        print(f"Could not parse: {args.filename}", file=sys.stderr)
        return 1

    print(f"\nParsed Anime File: {result.original_filename}")
    print(f"{'─' * 50}")
    print(f"Title:         {result.anime_title}")
    print(f"Season:        {result.season}")
    print(f"Episode:       {result.episode_number or 'N/A'}")
    print(f"Release Group: {result.release_group or 'N/A'}")
    print(f"Resolution:    {result.resolution or 'N/A'}")
    print(f"Source:        {result.video_source or 'N/A'}")

    return 0


def test_patterns(args: argparse.Namespace) -> int:
    """Test the parser against common anime filename patterns."""
    from plugins.anime_library_scanner_plugin.anime_library_scanner_plugin import (
        AnimeLibraryScannerPlugin,
        is_anitopy_available,
    )

    if not is_anitopy_available():
        print("Error: anitopy not installed.", file=sys.stderr)
        print("Install with: pip install anitopy>=2.1.1", file=sys.stderr)
        return 1

    test_filenames = [
        "[SubsPlease] Frieren - Beyond Journey's End - 01 (1080p) [A1B2C3D4].mkv",
        "[Erai-raws] Sousou no Frieren - 01 [1080p][Multiple Subtitle].mkv",
        "Demon Slayer - Kimetsu no Yaiba S04E01 [1080p BluRay x264].mkv",
        "[HorribleSubs] Attack on Titan - 01 [720p].mkv",
        "One Piece - 1089 (1080p WEB-DL) [SubsPlease].mkv",
        "[VCB-Studio] Bocchi the Rock! [01][Ma10p_1080p][x265_flac].mkv",
    ]

    plugin = AnimeLibraryScannerPlugin()
    print("Testing anime filename parsing patterns:\n")

    for filename in test_filenames:
        result = plugin.parse_filename(filename)
        if result:
            print(f"✓ {filename}")
            print(f"  → {result.anime_title} S{result.season:02d}E{result.episode_number or '??'}")
            if result.release_group:
                print(f"    Group: {result.release_group}, Res: {result.resolution or '?'}")
        else:
            print(f"✗ {filename}")
            print("  → Failed to parse")
        print()

    return 0


# ─────────────────────────────────────────────────────────────────────────────
# CLI Registration
# ─────────────────────────────────────────────────────────────────────────────


def register_cli() -> None:
    """Register anime_library_scanner_plugin commands with CLIManager."""
    cli = CLIManager()
    cli.register_module(
        ModuleRegistration(
            module_name="anime_library_scanner_plugin",
            short_name="als",
            description="Anime library scanner and filename parser",
            commands=[
                Command(
                    name="parse",
                    help="Parse an anime filename and show extracted metadata",
                    handler="plugins.anime_library_scanner_plugin.anime_library_scanner_plugin_cli:parse_filename",
                    args=[
                        CommandArg(
                            name="filename",
                            help="The anime filename to parse",
                        ),
                    ],
                ),
                Command(
                    name="test",
                    help="Test parser against common anime filename patterns",
                    handler="plugins.anime_library_scanner_plugin.anime_library_scanner_plugin_cli:test_patterns",
                ),
            ],
        )
    )
