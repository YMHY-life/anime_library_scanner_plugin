"""Anime library scanner plugin for parsing anime filenames.

This plugin integrates with external_media_manager to automatically parse
anime metadata from discovered media files using the anitopy library.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from plugins.anime_library_scanner_plugin.models import ParsedAnimeFile
from utils.logger_util import Logger

if TYPE_CHECKING:
    from managers.external_media_manager import ExternalMediaManager
    from managers.external_media_manager.models import MediaEvent

# Lazy import for optional anitopy dependency
try:
    import anitopy

    ANITOPY_AVAILABLE = True
except ImportError:
    anitopy = None  # type: ignore[assignment]
    ANITOPY_AVAILABLE = False


def is_anitopy_available() -> bool:
    """Check if anitopy library is available."""
    return ANITOPY_AVAILABLE


class AnimeLibraryScannerPlugin:
    """Plugin for scanning and parsing anime library files.

    Integrates with ExternalMediaManager's event system to receive
    FILE_DISCOVERED events and parse anime metadata from filenames.

    Attributes:
        on_parsed: Optional callback invoked when a file is successfully parsed.
                   Receives (MediaEvent, ParsedAnimeFile) as arguments.
    """

    def __init__(self) -> None:
        self.logger = Logger(name=__class__.__name__)
        self._subscription_id: Optional[str] = None
        self._media_manager: Optional["ExternalMediaManager"] = None

        # User-configurable callback for parsed files
        self.on_parsed: Optional[
            "callable[[MediaEvent, ParsedAnimeFile], None]"
        ] = None

        if not ANITOPY_AVAILABLE:
            self.logger.warning(
                "anitopy not installed. Install with: pip install anitopy>=2.1.1"
            )

    def parse_filename(self, filename: str) -> Optional[ParsedAnimeFile]:
        """Parse an anime filename into structured metadata.

        Args:
            filename: The filename to parse (not full path).

        Returns:
            ParsedAnimeFile if parsing succeeds, None if it fails or
            the filename doesn't match anime naming patterns.

        Example:
            >>> plugin = AnimeLibraryScannerPlugin()
            >>> result = plugin.parse_filename("[SubsPlease] Frieren - 01 (1080p).mkv")
            >>> result.anime_title
            'Frieren'
            >>> result.episode_number
            '01'
        """
        if not ANITOPY_AVAILABLE:
            self.logger.error("anitopy not available, cannot parse filename")
            return None

        try:
            parsed = anitopy.parse(filename)
        except Exception as e:
            self.logger.debug(f"Failed to parse '{filename}': {e}")
            return None

        if not parsed:
            self.logger.debug(f"No parse result for '{filename}'")
            return None

        # anitopy returns dict, extract relevant fields
        anime_title = parsed.get("anime_title")
        if not anime_title:
            self.logger.debug(f"No anime_title found in '{filename}'")
            return None

        # Handle season detection
        season = 1
        anime_season = parsed.get("anime_season")
        if anime_season:
            try:
                # anime_season can be string like "2" or list like ["2"]
                if isinstance(anime_season, list):
                    season = int(anime_season[0])
                else:
                    season = int(anime_season)
            except (ValueError, TypeError):
                pass

        # Handle episode number (can be string, list, or None)
        episode = parsed.get("episode_number")
        if isinstance(episode, list):
            episode = "-".join(str(e) for e in episode)
        elif episode is not None:
            episode = str(episode)

        return ParsedAnimeFile(
            original_filename=filename,
            anime_title=anime_title,
            episode_number=episode,
            season=season,
            release_group=parsed.get("release_group"),
            resolution=parsed.get("video_resolution"),
            video_source=parsed.get("source"),
        )

    def register_with_media_manager(
        self,
        media_manager: "ExternalMediaManager",
    ) -> str:
        """Register this plugin with an ExternalMediaManager.

        Subscribes to FILE_DISCOVERED events and automatically parses
        anime metadata from discovered files.

        Args:
            media_manager: The ExternalMediaManager instance to register with.

        Returns:
            The subscription ID (use to unregister later).

        Raises:
            RuntimeError: If already registered with a manager.
        """
        if self._subscription_id is not None:
            raise RuntimeError(
                "Already registered with a media manager. "
                "Call unregister() first."
            )

        from managers.external_media_manager import EventType

        self._media_manager = media_manager
        self._subscription_id = media_manager.subscribe(
            event_types=[EventType.FILE_DISCOVERED],
            callback=self._on_file_discovered,
        )

        self.logger.info("Registered with ExternalMediaManager")
        return self._subscription_id

    def unregister(self) -> bool:
        """Unregister from the current ExternalMediaManager.

        Returns:
            True if successfully unregistered, False if not registered.
        """
        if self._subscription_id is None or self._media_manager is None:
            return False

        result = self._media_manager.unsubscribe(self._subscription_id)
        self._subscription_id = None
        self._media_manager = None

        if result:
            self.logger.info("Unregistered from ExternalMediaManager")
        return result

    def _on_file_discovered(self, event: "MediaEvent") -> None:
        """Internal handler for FILE_DISCOVERED events.

        Args:
            event: The MediaEvent containing the discovered file.
        """
        if event.media_file is None:
            return

        filename = event.media_file.name
        parsed = self.parse_filename(filename)

        if parsed:
            self.logger.debug(
                f"Parsed: '{filename}' -> '{parsed.anime_title}' "
                f"S{parsed.season:02d}E{parsed.episode_number or '??'}"
            )

            # Invoke user callback if set
            if self.on_parsed:
                try:
                    self.on_parsed(event, parsed)
                except Exception as e:
                    self.logger.error(f"Error in on_parsed callback: {e}")
        else:
            self.logger.debug(f"Could not parse anime info from: '{filename}'")
