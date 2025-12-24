# Chromatographic Playlist

Many years ago I heard about a moving picture about people in a record shop. Perhaps it was _High Fidelity_. For some reason I understood that one of the 
characters sorted his music albums chromatographically, so thought that was a novel idea. I have since learned that this was not the case in that movie, but then again, why not?

So here it is, a tool to sort your playlists chromotographically by album cover art.

## Quick Start

```bash
uv run python -m chromalist get-playlist 3cEYpjA9oz9GiPac4AsH4n
uv run python -m chromalist process-images
uv run python -m chromalist generate-sorted-playlist
```

Run tests:

```bash
uv run pytest
```

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

### Command Line Interface
By default, all intermediate data (playlists, images _etc._) is stored in the `tmp/` directory.

#### Setting the Output Directory
You can use the `--output-dir {dir-name}` to specify the output directory for intermediate files. The default is `tmp/`.

#### Download a Playlist from Spotify
Download a playlist with a given ID and its album cover images to the output directory.

The playlist is called `playlist.json`, the images are named from their Spotify track IDs, `{track-id}.jpg`.

```bash
uv run python -m chromalist get-playlist {playlist-id}
```

#### Process Images
Run the image processing on the images in the output directory, writing a `image-colours.json` file there with the result.

```bash
uv run python -m chromalist process-images
```

#### Sort Playlist
Generate a chromatically sorted playlist from the `playlist.json` and the `image-colours.json` in the output directory 
writing a file `sorted-playlist.json` with the result.

```bash
uv run python -m chromalist generate-sorted-playlist
```

### Spotify API Tokens

You have to sign up for the Spotify Developer programme.
After that "Create an app" to get a client ID and client secret to sign in via the API.

## Example

It turns this:

<img src="https://i.scdn.co/image/ab67616d0000b273ce6d0eef0c1ce77e5f95bbbc" alt="Odiseo: Api" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273aa2ff29970d9a63a49dfaeb2" alt="Vlasta Marek: Is" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ee0d0dce888c6c8a70db6e8b" alt="LCD Soundsystem: All I Want" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2738b7447ac3daa1da18811cf7b" alt="Glenn Horiuchi: Endpoints" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27304e57d181ff062f8339d6c71" alt="Zucchero: You Are So Beautiful" width="64" height="64">

into this:

<img src="https://i.scdn.co/image/ab67616d0000b273ee0d0dce888c6c8a70db6e8b" alt="LCD Soundsystem: All I Want" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ce6d0eef0c1ce77e5f95bbbc" alt="Odiseo: Api" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27304e57d181ff062f8339d6c71" alt="Zucchero: You Are So Beautiful" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273aa2ff29970d9a63a49dfaeb2" alt="Vlasta Marek: Is" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2738b7447ac3daa1da18811cf7b" alt="Glenn Horiuchi: Endpoints" width="64" height="64">