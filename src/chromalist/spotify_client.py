from pathlib import Path

import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from chromalist.files import FilePaths
from chromalist.models import Playlist, Track


class SpotifyClient:
    """Client for interacting with Spotify API."""

    def __init__(self):
        """Initialize Spotify client with Client Credentials authentication.

        Environment variables required:
        - SPOTIPY_CLIENT_ID: Your Spotify application client ID
        - SPOTIPY_CLIENT_SECRET: Your Spotify application client secret
        """
        auth_manager = SpotifyClientCredentials()

        self.sp = spotipy.Spotify(auth_manager=auth_manager)

    def get_playlist(self, playlist_id: str) -> Playlist:
        """Fetch playlist metadata and tracks from Spotify.

        Args:
            playlist_id: Spotify playlist ID or full URI

        Returns:
            Playlist object containing metadata and tracks

        Raises:
            spotipy.SpotifyException: If playlist is not found or inaccessible
        """
        # Fetch playlist details
        playlist_data = self.sp.playlist(playlist_id)

        # Extract tracks
        tracks = []
        results = playlist_data["tracks"]

        while results:
            for item in results["items"]:
                if item["track"] is None:
                    # Skip local files or unavailable tracks
                    continue

                track_data = item["track"]

                # Get album art URL (prefer largest image)
                album_images = track_data["album"]["images"]
                album_art_url = album_images[0]["url"] if album_images else ""

                # Get artist name (first artist if multiple)
                artist_name = track_data["artists"][0]["name"] if track_data["artists"] else "Unknown"

                track = Track(
                    id=track_data["id"],
                    name=track_data["name"],
                    artist=artist_name,
                    album_name=track_data["album"]["name"],
                    album_art_url=album_art_url,
                )
                tracks.append(track)

            # Check if there are more tracks to fetch
            if results["next"]:
                results = self.sp.next(results)
            else:
                results = None

        playlist = Playlist(
            id=playlist_data["id"],
            name=playlist_data["name"],
            description=playlist_data.get("description", ""),
            tracks=tracks,
        )

        return playlist

    def download_album_art(self, track_id: str, image_url: str, file_paths: FilePaths) -> None:
        """Download album art image and save to file.

        Args:
            track_id: Spotify track ID (used for filename)
            image_url: URL of the album art image
            file_paths: FilePaths instance for managing paths

        Raises:
            requests.RequestException: If download fails
        """
        if not image_url:
            return

        response = requests.get(image_url, timeout=10)
        response.raise_for_status()

        # Save as JPEG
        filepath = file_paths.track_image_path(track_id)
        with open(filepath, "wb") as f:
            f.write(response.content)
