# Anime Library Scanner Plugin

## Overview
Parses anime filenames to extract structured metadata using the [anitopy](https://github.com/igorcmoura/anitopy) library. Integrates with `external_media_manager` to automatically process discovered anime files.

## Features
- Parse anime filenames into structured metadata (title, episode, season, release group, resolution)
- Event-driven integration with `external_media_manager`
- CLI commands for testing and debugging
- Callback system for custom processing of parsed files

## Usage

### Standalone Parsing
```python
from plugins.anime_library_scanner_plugin import AnimeLibraryScannerPlugin

plugin = AnimeLibraryScannerPlugin()
result = plugin.parse_filename("[SubsPlease] Frieren - 01 (1080p).mkv")

print(result.anime_title)      # "Frieren"
print(result.episode_number)   # "01"
print(result.resolution)       # "1080p"
print(result.release_group)    # "SubsPlease"
```

### Integration with ExternalMediaManager
```python
from managers.external_media_manager import ExternalMediaManager
from plugins.anime_library_scanner_plugin import AnimeLibraryScannerPlugin

manager = ExternalMediaManager()
scanner = AnimeLibraryScannerPlugin()

# Set up callback for parsed files
def on_parsed(event, parsed):
    print(f"Found: {parsed.anime_title} S{parsed.season}E{parsed.episode_number}")

scanner.on_parsed = on_parsed
scanner.register_with_media_manager(manager)

# Scan triggers FILE_DISCOVERED events -> plugin parses filenames
manager.scan_folder("/media/anime")
```

### CLI Commands
```bash
# Parse a single filename
./adhd_framework.py als parse "[SubsPlease] Frieren - 01 (1080p).mkv"

# Test parser with common patterns
./adhd_framework.py als test
```

## Module Structure

```
anime_library_scanner_plugin/
├── __init__.py                       # Module exports
├── anime_library_scanner_plugin.py   # Main plugin class
├── anime_library_scanner_plugin_cli.py # CLI commands
├── models.py                         # ParsedAnimeFile model
├── init.yaml                         # Module metadata
├── requirements.txt                  # PyPI: anitopy
├── refresh.py                        # CLI registration
├── README.md                         # This file
├── tests/                            # Unit tests
└── playground/                       # Demo scripts
```


## Testing

### Unit Tests (Optional)
```bash
pytest <module_type>/<module_name>/tests/
```

### Adversarial Testing
HyperRed will attack this module based on `testing.scope` in `init.yaml`.
Configure threat_model: `internal` | `external` | `adversarial`