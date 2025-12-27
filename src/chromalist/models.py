import json
from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class Track:
    id: str
    name: str
    artist: str
    album_name: str
    album_art_url: str
    hue: float | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert Track to dictionary for JSON serialization."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Track":
        """Create Track from dictionary."""
        return cls(**data)


@dataclass
class Playlist:
    id: str
    name: str
    description: str
    tracks: list[Track]

    def to_dict(self) -> dict[str, Any]:
        """Convert Playlist to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "tracks": [track.to_dict() for track in self.tracks],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Playlist":
        """Create Playlist from dictionary."""
        tracks = [Track.from_dict(t) for t in data["tracks"]]
        return cls(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            tracks=tracks,
        )

    def to_json(self, filepath: str | Path) -> None:
        """Save playlist to JSON file."""
        with open(filepath, "w") as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def from_json(cls, filepath: str | Path) -> "Playlist":
        """Load playlist from JSON file."""
        with open(filepath, "r") as f:
            data = json.load(f)
        return cls.from_dict(data)


@dataclass
class ImageColorData:
    track_id: str
    rgbs: list[tuple[int, int, int]]
    hsvs: list[tuple[float, float, float]]
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert ImageColorData to dictionary for JSON serialization."""
        return {
            "track_id": self.track_id,
            "rgbs": self.rgbs,
            "hsvs": self.hsvs,
            "error": self.error,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ImageColorData":
        """Create ImageColorData from dictionary."""
        return cls(
            track_id=data["track_id"],
            rgbs=[tuple(rgb) for rgb in data["rgbs"]],
            hsvs=[tuple(hsv) for hsv in data["hsvs"]],
            error=data.get("error"),
        )
