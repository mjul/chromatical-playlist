# Responsible for file paths

from pathlib import Path


class FilePaths:
    """Responsible for managing paths to the application data files."""

    def __init__(self, path: Path):
        if not path.exists():
            raise FileNotFoundError("Output directory does not exist", path)
        self.path = path

    def playlist_path(self) -> Path:
        return self.path / "playlist.json"

    def track_image_path(self, track_id: str) -> Path:
        return self.path / f"{track_id}.jpg"

    def image_colours_path(self) -> Path:
        return self.path / "image-colours.json"

    def sorted_playlist_path(self) -> Path:
        return self.path / "sorted-playlist.json"

    def sorted_playlist_images_markdown_path(self) -> Path:
        return self.path / "sorted-playlist-images.md"
