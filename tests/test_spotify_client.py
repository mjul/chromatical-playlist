"""Tests for Spotify client functionality."""
from unittest.mock import Mock, patch

import pytest

from chromalist.models import Playlist
from chromalist.spotify_client import SpotifyClient


@pytest.fixture
def mock_spotify_data():
    """Mock data returned from Spotify API."""
    return {
        "id": "test_playlist_id",
        "name": "Test Playlist",
        "description": "A test playlist for unit tests",
        "tracks": {
            "items": [
                {
                    "track": {
                        "id": "track1",
                        "name": "Test Song 1",
                        "artists": [{"name": "Test Artist 1"}],
                        "album": {
                            "name": "Test Album 1",
                            "images": [{"url": "http://example.com/image1.jpg"}],
                        },
                    }
                },
                {
                    "track": {
                        "id": "track2",
                        "name": "Test Song 2",
                        "artists": [{"name": "Test Artist 2"}],
                        "album": {
                            "name": "Test Album 2",
                            "images": [{"url": "http://example.com/image2.jpg"}],
                        },
                    }
                },
            ],
            "next": None,
        },
    }


@pytest.fixture
def mock_spotify_client():
    """Create a SpotifyClient with mocked spotipy."""
    with patch("chromalist.spotify_client.spotipy.Spotify") as mock_sp:
        with patch("chromalist.spotify_client.SpotifyOAuth"):
            client = SpotifyClient()
            client.sp = mock_sp.return_value
            yield client


def test_spotify_client_initialization():
    """Test that SpotifyClient initializes with OAuth."""
    with patch("chromalist.spotify_client.spotipy.Spotify") as mock_sp:
        with patch("chromalist.spotify_client.SpotifyOAuth") as mock_auth:
            _ = SpotifyClient()

            # Verify OAuth was created with correct scope
            mock_auth.assert_called_once()
            call_kwargs = mock_auth.call_args[1]
            assert "playlist-read-private" in call_kwargs["scope"]
            assert call_kwargs["open_browser"] is True

            # Verify Spotify client was created with auth manager
            mock_sp.assert_called_once()


def test_get_playlist_success(mock_spotify_client, mock_spotify_data):
    """Test successfully fetching a playlist."""
    mock_spotify_client.sp.playlist.return_value = mock_spotify_data

    playlist = mock_spotify_client.get_playlist("test_playlist_id")

    # Verify API was called
    mock_spotify_client.sp.playlist.assert_called_once_with("test_playlist_id")

    # Verify playlist data
    assert isinstance(playlist, Playlist)
    assert playlist.id == "test_playlist_id"
    assert playlist.name == "Test Playlist"
    assert playlist.description == "A test playlist for unit tests"
    assert len(playlist.tracks) == 2

    # Verify track data
    track1 = playlist.tracks[0]
    assert track1.id == "track1"
    assert track1.name == "Test Song 1"
    assert track1.artist == "Test Artist 1"
    assert track1.album_name == "Test Album 1"
    assert track1.album_art_url == "http://example.com/image1.jpg"


def test_get_playlist_with_null_tracks(mock_spotify_client):
    """Test that null tracks (local files) are skipped."""
    mock_data = {
        "id": "test_playlist_id",
        "name": "Test Playlist",
        "description": "Test",
        "tracks": {
            "items": [
                {"track": None},  # Local file or unavailable track
                {
                    "track": {
                        "id": "track1",
                        "name": "Test Song 1",
                        "artists": [{"name": "Test Artist 1"}],
                        "album": {
                            "name": "Test Album 1",
                            "images": [{"url": "http://example.com/image1.jpg"}],
                        },
                    }
                },
            ],
            "next": None,
        },
    }

    mock_spotify_client.sp.playlist.return_value = mock_data

    playlist = mock_spotify_client.get_playlist("test_playlist_id")

    # Should only have 1 track (the null track should be skipped)
    assert len(playlist.tracks) == 1
    assert playlist.tracks[0].id == "track1"


def test_get_playlist_pagination(mock_spotify_client):
    """Test fetching playlist with multiple pages of tracks."""
    # First page
    first_page = {
        "id": "test_playlist_id",
        "name": "Test Playlist",
        "description": "Test",
        "tracks": {
            "items": [
                {
                    "track": {
                        "id": "track1",
                        "name": "Test Song 1",
                        "artists": [{"name": "Artist 1"}],
                        "album": {
                            "name": "Album 1",
                            "images": [{"url": "http://example.com/image1.jpg"}],
                        },
                    }
                },
            ],
            "next": "http://api.spotify.com/next",
        },
    }

    # Second page
    second_page = {
        "items": [
            {
                "track": {
                    "id": "track2",
                    "name": "Test Song 2",
                    "artists": [{"name": "Artist 2"}],
                    "album": {
                        "name": "Album 2",
                        "images": [{"url": "http://example.com/image2.jpg"}],
                    },
                }
            },
        ],
        "next": None,
    }

    mock_spotify_client.sp.playlist.return_value = first_page
    mock_spotify_client.sp.next.return_value = second_page

    playlist = mock_spotify_client.get_playlist("test_playlist_id")

    # Should have tracks from both pages
    assert len(playlist.tracks) == 2
    assert playlist.tracks[0].id == "track1"
    assert playlist.tracks[1].id == "track2"
    mock_spotify_client.sp.next.assert_called_once()


def test_download_album_art_success(mock_spotify_client, tmp_path):
    """Test successfully downloading album art."""
    mock_response = Mock()
    mock_response.content = b"fake_image_data"

    with patch("chromalist.spotify_client.requests.get", return_value=mock_response):
        mock_spotify_client.download_album_art(
            "track123",
            "http://example.com/image.jpg",
            tmp_path
        )

    # Verify file was created
    output_file = tmp_path / "track123.jpg"
    assert output_file.exists()
    assert output_file.read_bytes() == b"fake_image_data"


def test_download_album_art_empty_url(mock_spotify_client, tmp_path):
    """Test that empty URL is handled gracefully."""
    # Should not raise an error, just return early
    mock_spotify_client.download_album_art("track123", "", tmp_path)

    # No file should be created
    output_file = tmp_path / "track123.jpg"
    assert not output_file.exists()


def test_download_album_art_network_error(mock_spotify_client, tmp_path):
    """Test handling of network errors during download."""
    import requests

    with patch("chromalist.spotify_client.requests.get") as mock_get:
        mock_get.side_effect = requests.RequestException("Network error")

        with pytest.raises(requests.RequestException):
            mock_spotify_client.download_album_art(
                "track123",
                "http://example.com/image.jpg",
                tmp_path
            )
