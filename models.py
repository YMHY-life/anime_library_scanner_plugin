"""Data models for anime_library_scanner_plugin."""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class ParsedAnimeFile(BaseModel):
    """Represents parsed anime metadata extracted from a filename.

    Uses anitopy library for parsing anime filenames into structured data.
    """

    original_filename: str = Field(description="The original filename that was parsed")
    anime_title: str = Field(description="The detected anime title")
    episode_number: Optional[str] = Field(
        default=None,
        description="Episode number (can be range like '01-12' or special format)",
    )
    season: int = Field(default=1, description="Season number, defaults to 1")
    release_group: Optional[str] = Field(
        default=None,
        description="Fansub/release group name (e.g., 'SubsPlease', 'Erai-raws')",
    )
    resolution: Optional[str] = Field(
        default=None,
        description="Video resolution (e.g., '1080p', '720p', '4K')",
    )
    video_source: Optional[str] = Field(
        default=None,
        description="Video source type (e.g., 'BluRay', 'WEB', 'HDTV')",
    )

    class Config:
        """Pydantic model configuration."""

        frozen = True  # Immutable after creation
