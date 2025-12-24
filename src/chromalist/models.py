from dataclasses import dataclass

@dataclass
class Track:
    id: str
    name: str
    album_art_url: str
    hue: float | None = None
