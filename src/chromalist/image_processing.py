import colorsys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy.cluster.vq import kmeans

from chromalist.files import FilePaths
from chromalist.models import ImageColourData, Playlist


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
                + (
                    f" and {len(missing_files) - 5} more..."
                    if len(missing_files) > 5
                    else ""
                )
            )

    def extract_colours(
        self, image_path: Path, k: int = 3
    ) -> tuple[list[tuple[int, int, int]], list[tuple[float, float, float]]]:
        """Extract k dominant colours from an image.

        Args:
            image_path: Path to the image file
            k: Number of dominant colours to extract

        Returns:
            Tuple of (RGB colour list, HSV colour list) sorted by frequency (descending)
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

        # Run k-means clustering to find k dominant colours
        centroids, _ = kmeans(pixels_float, k)

        # Convert centroids back to integers for RGB
        rgb_colours = [tuple(map(int, centroid)) for centroid in centroids]

        # Calculate frequency of each cluster to sort by dominance
        from scipy.cluster.vq import vq

        codes, _ = vq(pixels_float, centroids)
        unique, counts = np.unique(codes, return_counts=True)

        # Sort colours by frequency (descending)
        sorted_indices = np.argsort(-counts)
        rgb_colours = [rgb_colours[i] for i in sorted_indices]

        # Convert RGB to HSV
        hsv_colours = []
        for r, g, b in rgb_colours:
            # Normalize RGB to 0-1 for colorsys
            h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
            # Convert to degrees and percentages
            hsv_colours.append((h * 360, s * 100, v * 100))

        return rgb_colours, hsv_colours

    def process_track(self, file_paths: FilePaths, k, track) -> ImageColourData:
        image_path = file_paths.track_image_path(track.id)

        try:
            rgbs, hsvs = self.extract_colours(image_path, k)
            result = ImageColourData(
                track_id=track.id, rgbs=rgbs, hsvs=hsvs, error=None
            )
        except Exception as e:
            # Flag error but continue processing
            result = ImageColourData(
                track_id=track.id, rgbs=[], hsvs=[], error=str(e))

        return result
