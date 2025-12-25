"""Playlist sorting by dominant color hue."""

import json
from pathlib import Path

from chromalist.models import ImageColorData, Playlist


def sort_playlist_by_hue(output_dir: Path) -> tuple[Playlist, int]:
    """
    Sort a playlist by the hue of the dominant color in album cover art.

    Reads playlist.json and image-colours.json from output_dir, sorts tracks
    by the hue component (0-360°) of the most dominant color, and writes
    the sorted playlist to sorted-playlist.json.

    Tracks without valid color data (missing or with errors) are excluded
    from the sorted output.

    Args:
        output_dir: Directory containing playlist.json and image-colours.json

    Returns:
        Tuple of (sorted_playlist, excluded_count) where excluded_count is the
        number of tracks that couldn't be sorted due to missing/invalid color data

    Raises:
        FileNotFoundError: If playlist.json or image-colours.json don't exist
        json.JSONDecodeError: If JSON files are malformed
    """
    # Validate input files exist
    playlist_path = output_dir / "playlist.json"
    if not playlist_path.exists():
        raise FileNotFoundError(
            f"Playlist file not found: {playlist_path}\n"
            "Please run 'get-playlist' first to download playlist data."
        )

    colors_path = output_dir / "image-colours.json"
    if not colors_path.exists():
        raise FileNotFoundError(
            f"Image colors file not found: {colors_path}\n"
            "Please run 'process-images' first to extract color data."
        )

    # Load playlist
    playlist = Playlist.from_json(str(playlist_path))

    # Load color data
    with open(colors_path, "r") as f:
        colors_data_raw = json.load(f)

    # Parse color data into ImageColorData objects and create track_id -> hue mapping
    track_hues: dict[str, float] = {}
    for item in colors_data_raw:
        color_data = ImageColorData.from_dict(item)

        # Skip tracks with errors or missing color data
        if color_data.error is not None or not color_data.hsvs:
            continue

        # Extract hue from the most dominant color (first in list)
        hue = color_data.hsvs[0][0]  # First color, first component (hue)
        track_hues[color_data.track_id] = hue

    # Separate tracks into sortable and excluded
    sortable_tracks = []
    excluded_tracks = []

    for track in playlist.tracks:
        if track.id in track_hues:
            # Set the hue field for transparency
            track.hue = track_hues[track.id]
            sortable_tracks.append(track)
        else:
            excluded_tracks.append(track)

    # Sort tracks by hue (0-360°)
    sortable_tracks.sort(
        key=lambda t: t.hue if t.hue is not None else float('inf'))

    # Create sorted playlist with same metadata but reordered tracks
    sorted_playlist = Playlist(
        id=playlist.id,
        name=playlist.name,
        description=playlist.description,
        tracks=sortable_tracks
    )

    # Write sorted playlist to output file
    output_path = output_dir / "sorted-playlist.json"
    sorted_playlist.to_json(str(output_path))

    # Write a list of the images as markdown (so we can show them in the README)
    images_md_path = output_dir / "sorted-playlist-images.md"
    with open(images_md_path, "w") as f:
        for track in sortable_tracks:
            f.write(
                f'<img src="{track.album_art_url}" alt="{track.name} ({track.artist})" width="64" height="64">\n')

    return sorted_playlist, len(excluded_tracks)
