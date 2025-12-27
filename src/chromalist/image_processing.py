import colorsys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy.cluster.vq import kmeans

from chromalist.files import FilePaths
from chromalist.models import ImageColorData, Playlist


class ImageProcessor:
    def __init__(self):
        pass

    def validate_files(self, file_paths: FilePaths, playlist: Playlist) -> None:
        """Validate that all required image files exist.

        Args:
            file_paths: FilePaths instance for managing paths
            playlist: Playlist object with track information

        Raises:
            FileNotFoundError: If any required image file is missing
        """
        missing_files = []
        for track in playlist.tracks:
            image_path = file_paths.track_image_path(track.id)
            if not image_path.exists():
                missing_files.append(str(image_path))

        if missing_files:
            raise FileNotFoundError(
                f"Missing {len(missing_files)} image file(s). "
                f"Please run 'get-playlist' first to download images.\n"
                f"Missing files: {', '.join(missing_files[:5])}"
                + (f" and {len(missing_files) - 5} more..." if len(missing_files) > 5 else "")
            )

    def extract_colors(self, image_path: Path, k: int = 3) -> tuple[list[tuple[int, int, int]], list[tuple[float, float, float]]]:
        """Extract k dominant colors from an image.

        Args:
            image_path: Path to the image file
            k: Number of dominant colors to extract

        Returns:
            Tuple of (RGB color list, HSV color list) sorted by frequency (descending)
            RGB values are in range 0-255
            HSV values are (H: 0-360, S: 0-100, V: 0-100)
        """
        # Load image and convert to RGB
        img = Image.open(image_path)
        img = img.convert("RGB")

        # Convert to numpy array and reshape to list of pixels
        pixels = np.array(img)
        pixels_reshaped = pixels.reshape(-1, 3)

        # Convert to float for k-means
        pixels_float = pixels_reshaped.astype(float)

        # Run k-means clustering to find k dominant colors
        centroids, _ = kmeans(pixels_float, k)

        # Convert centroids back to integers for RGB
        rgb_colors = [tuple(map(int, centroid)) for centroid in centroids]

        # Calculate frequency of each cluster to sort by dominance
        from scipy.cluster.vq import vq
        codes, _ = vq(pixels_float, centroids)
        unique, counts = np.unique(codes, return_counts=True)

        # Sort colors by frequency (descending)
        sorted_indices = np.argsort(-counts)
        rgb_colors = [rgb_colors[i] for i in sorted_indices]

        # Convert RGB to HSV
        hsv_colors = []
        for r, g, b in rgb_colors:
            # Normalize RGB to 0-1 for colorsys
            h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
            # Convert to degrees and percentages
            hsv_colors.append((h * 360, s * 100, v * 100))

        return rgb_colors, hsv_colors

    def process_playlist(self, file_paths: FilePaths, k: int = 3) -> list[ImageColorData]:
        """Process all images in a playlist to extract dominant colors.

        Args:
            file_paths: FilePaths instance for managing paths
            k: Number of dominant colors to extract per image

        Returns:
            List of ImageColorData objects, one per track

        Raises:
            FileNotFoundError: If playlist.json or any image files are missing
        """
        # Load playlist
        playlist_path = file_paths.playlist_path()
        if not playlist_path.exists():
            raise FileNotFoundError(
                f"Playlist file not found: {playlist_path}\n"
                "Please run 'get-playlist' first to download playlist data."
            )

        playlist = Playlist.from_json(playlist_path)

        # Validate all image files exist
        self.validate_files(file_paths, playlist)

        # Process each track's image
        results = []
        for track in playlist.tracks:
            results.append(self.proces_track(file_paths, k, track))

        return results

    def proces_track(self, file_paths: FilePaths, k, track) -> ImageColorData:
        image_path = file_paths.track_image_path(track.id)

        try:
            rgbs, hsvs = self.extract_colors(image_path, k)
            result = ImageColorData(
                track_id=track.id,
                rgbs=rgbs,
                hsvs=hsvs,
                error=None
            )
        except Exception as e:
            # Flag error but continue processing
            result = ImageColorData(
                track_id=track.id,
                rgbs=[],
                hsvs=[],
                error=str(e)
            )

        return result
