# Chromatographic Playlist

Many years ago I heard about a moving picture about people in a record shop. Perhaps it was _High Fidelity_. For some reason I understood that one of the 
characters sorted his music albums chromatographically, so thought that was a novel idea. I have since learned that this was not the case in that movie, but then again, why not?

So here it is, a tool to sort your playlists chromotographically by album cover art.

## How it works

- fetch a playlist from Spotify (note: API token required)
- get the album cover art for each song
- use the _k-means clustering_ algorithm to extract the dominant _k_ colours from the cover image
- map the top colour to HSV colour space, and use the Hue component as a unidimensional scalar we can sort by
- emit the chromatographically sorted playlist

## Implementation

- Python: we use Python as the implementation language, because it has very good image processing libraries.
- Sci-Py: we use the _k-means algorithm_ from there
- Astral `uv`: a quick way to manage the Python packages (https://docs.astral.sh/uv/)
- Astral `ty`: the type-checker (see https://docs.astral.sh/ty/)
- Typer: for parsing the CLI (see https://typer.tiangolo.com/)
- Docker: This project runs in a Docker container

### Source Layout

```
project_root/
├── pyproject.toml       # Configuration for uv, deps, and tool settings
├── src/
│   └── chromalist/      
│       ├── __init__.py          # Empty, no exports
│       ├── __main__.py          # Allows `python -m chromalist`
│       ├── cli.py               # Command-line interface logic (click/typer)
│       ├── spotify_client.py    # Spotify client for downloading the playlists and album art
│       ├── image_processing.py  # Image processing logic
│       └── models.py            # A bit overkill, but this is the domain model
└── tests/                       # Tests code for the various files above
```