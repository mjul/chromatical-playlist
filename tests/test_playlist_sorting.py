"""Tests for playlist sorting by hue."""

import json

import pytest

from chromalist.files import FilePaths
from chromalist.models import ImageColourData, Playlist, Track
from chromalist.playlist_sorting import sort_playlist_by_hue


@pytest.fixture
def sample_playlist():
    """Create a sample playlist with 3 tracks."""
    return Playlist(
        id="test_playlist_123",
        name="Test Playlist",
        description="A test playlist for sorting",
        tracks=[
            Track(
                id="track_red",
                name="Red Song",
                artist="Artist A",
                album_name="Red Album",
                album_art_url="https://example.com/red.jpg",
            ),
            Track(
                id="track_green",
                name="Green Song",
                artist="Artist B",
                album_name="Green Album",
                album_art_url="https://example.com/green.jpg",
            ),
            Track(
                id="track_blue",
                name="Blue Song",
                artist="Artist C",
                album_name="Blue Album",
                album_art_url="https://example.com/blue.jpg",
            ),
        ],
    )


@pytest.fixture
def sample_color_data():
    """Create sample colour data for 3 tracks with different hues."""
    return [
        # Red: hue ~0°
        ImageColourData(
            track_id="track_red",
            rgbs=[(255, 0, 0), (200, 50, 50), (150, 100, 100)],
            hsvs=[(0.0, 100.0, 100.0), (15.0, 75.0, 78.4), (0.0, 33.3, 58.8)],
            error=None,
        ),
        # Green: hue ~120°
        ImageColourData(
            track_id="track_green",
            rgbs=[(0, 255, 0), (50, 200, 50), (100, 150, 100)],
            hsvs=[(120.0, 100.0, 100.0),
                  (120.0, 75.0, 78.4), (120.0, 33.3, 58.8)],
            error=None,
        ),
        # Blue: hue ~240°
        ImageColourData(
            track_id="track_blue",
            rgbs=[(0, 0, 255), (50, 50, 200), (100, 100, 150)],
            hsvs=[(240.0, 100.0, 100.0),
                  (240.0, 75.0, 78.4), (240.0, 33.3, 58.8)],
            error=None,
        ),
    ]


def test_sort_playlist_missing_playlist_file(tmp_path):
    """Test that missing playlist.json raises FileNotFoundError."""
    file_paths = FilePaths(tmp_path)
    # Create colors file but not playlist
    colours_file = file_paths.image_colours_path()
    colours_file.write_text("[]")

    with pytest.raises(FileNotFoundError) as exc_info:
        sort_playlist_by_hue(file_paths)

    assert "playlist.json" in str(exc_info.value).lower()
    assert "get-playlist" in str(exc_info.value).lower()


def test_sort_playlist_missing_colors_file(tmp_path, sample_playlist):
    """Test that missing image-colours.json raises FileNotFoundError."""
    file_paths = FilePaths(tmp_path)
    # Create playlist file but not colors
    playlist_file = file_paths.playlist_path()
    sample_playlist.to_json(playlist_file)

    with pytest.raises(FileNotFoundError) as exc_info:
        sort_playlist_by_hue(file_paths)

    assert "image-colours.json" in str(exc_info.value).lower()
    assert "process-images" in str(exc_info.value).lower()


def test_sort_playlist_success(tmp_path, sample_playlist, sample_color_data):
    """Test successful sorting of playlist by hue."""
    file_paths = FilePaths(tmp_path)
    # Write input files
    playlist_file = file_paths.playlist_path()
    sample_playlist.to_json(playlist_file)

    colours_file = file_paths.image_colours_path()
    with open(colours_file, "w") as f:
        json.dump([c.to_dict() for c in sample_color_data], f)

    # Sort playlist
    sorted_playlist, excluded_count = sort_playlist_by_hue(file_paths)

    # Verify output file was created
    output_file = file_paths.sorted_playlist_path()
    assert output_file.exists()

    # Verify no tracks were excluded
    assert excluded_count == 0
    assert len(sorted_playlist.tracks) == 3

    # Verify tracks are sorted by hue: red (0°) < green (120°) < blue (240°)
    assert sorted_playlist.tracks[0].id == "track_red"
    assert sorted_playlist.tracks[1].id == "track_green"
    assert sorted_playlist.tracks[2].id == "track_blue"

    # Verify hue values were populated
    assert sorted_playlist.tracks[0].sort_key == (0,0.0)
    assert sorted_playlist.tracks[1].sort_key == (0,120.0)
    assert sorted_playlist.tracks[2].sort_key == (0,240.0)

    # Verify playlist metadata is preserved
    assert sorted_playlist.id == sample_playlist.id
    assert sorted_playlist.name == sample_playlist.name
    assert sorted_playlist.description == sample_playlist.description

    # Verify output file can be read back
    loaded_playlist = Playlist.from_json(output_file)
    assert loaded_playlist.id == sample_playlist.id
    assert len(loaded_playlist.tracks) == 3


def test_sort_playlist_with_missing_color_data(
    tmp_path, sample_playlist, sample_color_data
):
    """Test that tracks without color data are excluded from sorted output."""
    file_paths = FilePaths(tmp_path)
    # Remove colour data for one track
    colour_data_subset = [
        c for c in sample_color_data if c.track_id != "track_green"]

    # Write input files
    playlist_file = file_paths.playlist_path()
    sample_playlist.to_json(playlist_file)

    colours_file = file_paths.image_colours_path()
    with open(colours_file, "w") as f:
        json.dump([c.to_dict() for c in colour_data_subset], f)

    # Sort playlist
    sorted_playlist, excluded_count = sort_playlist_by_hue(file_paths)

    # Verify one track was excluded
    assert excluded_count == 1
    assert len(sorted_playlist.tracks) == 2

    # Verify only tracks with color data are in output
    track_ids = [t.id for t in sorted_playlist.tracks]
    assert "track_red" in track_ids
    assert "track_blue" in track_ids
    assert "track_green" not in track_ids


def test_sort_playlist_with_error_in_color_data(
    tmp_path, sample_playlist, sample_color_data
):
    """Test that tracks with errors in colour extraction are excluded."""
    file_paths = FilePaths(tmp_path)
    # Set error on one track
    sample_color_data[1].error = "Failed to process image"
    sample_color_data[1].hsvs = []

    # Write input files
    playlist_file = file_paths.playlist_path()
    sample_playlist.to_json(playlist_file)

    colours_file = file_paths.image_colours_path()
    with open(colours_file, "w") as f:
        json.dump([c.to_dict() for c in sample_color_data], f)

    # Sort playlist
    sorted_playlist, excluded_count = sort_playlist_by_hue(file_paths)

    # Verify one track was excluded
    assert excluded_count == 1
    assert len(sorted_playlist.tracks) == 2

    # Verify track with error is not in output
    track_ids = [t.id for t in sorted_playlist.tracks]
    assert "track_green" not in track_ids


def test_sort_playlist_empty_playlist(tmp_path):
    """Test sorting an empty playlist."""
    file_paths = FilePaths(tmp_path)
    empty_playlist = Playlist(
        id="empty_playlist",
        name="Empty Playlist",
        description="No tracks",
        tracks=[],
    )

    # Write input files
    playlist_file = file_paths.playlist_path()
    empty_playlist.to_json(playlist_file)

    colours_file = file_paths.image_colours_path()
    with open(colours_file, "w") as f:
        json.dump([], f)

    # Sort playlist
    sorted_playlist, excluded_count = sort_playlist_by_hue(file_paths)

    # Verify results
    assert excluded_count == 0
    assert len(sorted_playlist.tracks) == 0
    assert sorted_playlist.id == empty_playlist.id


def test_sort_playlist_single_track(tmp_path):
    """Test sorting a playlist with a single track."""
    file_paths = FilePaths(tmp_path)
    single_track_playlist = Playlist(
        id="single_playlist",
        name="Single Track",
        description="One track only",
        tracks=[
            Track(
                id="track_1",
                name="Only Song",
                artist="Solo Artist",
                album_name="Solo Album",
                album_art_url="https://example.com/solo.jpg",
            )
        ],
    )

    colour_data = [
        ImageColourData(
            track_id="track_1",
            rgbs=[(128, 64, 192)],
            hsvs=[(270.0, 66.7, 75.3)],
            error=None,
        )
    ]

    # Write input files
    playlist_file = file_paths.playlist_path()
    single_track_playlist.to_json(playlist_file)

    colours_file = file_paths.image_colours_path()
    with open(colours_file, "w") as f:
        json.dump([c.to_dict() for c in colour_data], f)

    # Sort playlist
    sorted_playlist, excluded_count = sort_playlist_by_hue(file_paths)

    # Verify results
    assert excluded_count == 0
    assert len(sorted_playlist.tracks) == 1
    assert sorted_playlist.tracks[0].id == "track_1"
    assert sorted_playlist.tracks[0].sort_key == (0,270.0)


def test_sort_playlist_hue_order(tmp_path):
    """Test that tracks are sorted correctly across the full hue spectrum."""
    file_paths = FilePaths(tmp_path)
    # Create playlist with tracks spanning the hue spectrum
    playlist = Playlist(
        id="spectrum_playlist",
        name="Colour Spectrum",
        description="Full colour range",
        tracks=[
            Track(
                id="track_yellow",
                name="Yellow",
                artist="A",
                album_name="Album",
                album_art_url="http://example.com/1.jpg",
            ),
            Track(
                id="track_magenta",
                name="Magenta",
                artist="A",
                album_name="Album",
                album_art_url="http://example.com/2.jpg",
            ),
            Track(
                id="track_cyan",
                name="Cyan",
                artist="A",
                album_name="Album",
                album_art_url="http://example.com/3.jpg",
            ),
            Track(
                id="track_orange",
                name="Orange",
                artist="A",
                album_name="Album",
                album_art_url="http://example.com/4.jpg",
            ),
        ],
    )

    colour_data = [
        ImageColourData(
            track_id="track_yellow", rgbs=[], hsvs=[(60.0, 100.0, 100.0)], error=None
        ),
        ImageColourData(
            track_id="track_magenta", rgbs=[], hsvs=[(300.0, 100.0, 100.0)], error=None
        ),
        ImageColourData(
            track_id="track_cyan", rgbs=[], hsvs=[(180.0, 100.0, 100.0)], error=None
        ),
        ImageColourData(
            track_id="track_orange", rgbs=[], hsvs=[(30.0, 100.0, 100.0)], error=None
        ),
    ]

    # Write input files
    playlist_file = file_paths.playlist_path()
    playlist.to_json(playlist_file)

    colours_file = file_paths.image_colours_path()
    with open(colours_file, "w") as f:
        json.dump([c.to_dict() for c in colour_data], f)

    # Sort playlist
    sorted_playlist, excluded_count = sort_playlist_by_hue(file_paths)

    # Verify correct order: orange (30°) < yellow (60°) < cyan (180°) < magenta (300°)
    assert len(sorted_playlist.tracks) == 4
    assert sorted_playlist.tracks[0].id == "track_orange"
    assert sorted_playlist.tracks[1].id == "track_yellow"
    assert sorted_playlist.tracks[2].id == "track_cyan"
    assert sorted_playlist.tracks[3].id == "track_magenta"

    # Verify hue values are correct
    assert sorted_playlist.tracks[0].sort_key == (0,30.0)
    assert sorted_playlist.tracks[1].sort_key == (0,60.0)
    assert sorted_playlist.tracks[2].sort_key == (0,180.0)
    assert sorted_playlist.tracks[3].sort_key == (0,300.0)
