import tempfile
from pathlib import Path

import pytest
from PIL import Image

from chromalist.files import FilePaths
from chromalist.image_processing import ImageProcessor
from chromalist.models import ImageColorData, Playlist, Track


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_playlist():
    """Create a sample playlist for testing."""
    return Playlist(
        id="test_playlist_id",
        name="Test Playlist",
        description="A test playlist",
        tracks=[
            Track(
                id="track1",
                name="Song 1",
                artist="Artist 1",
                album_name="Album 1",
                album_art_url="https://example.com/art1.jpg",
            ),
            Track(
                id="track2",
                name="Song 2",
                artist="Artist 2",
                album_name="Album 2",
                album_art_url="https://example.com/art2.jpg",
            ),
            Track(
                id="track3",
                name="Song 3",
                artist="Artist 3",
                album_name="Album 3",
                album_art_url="https://example.com/art3.jpg",
            ),
        ],
    )


@pytest.fixture
def create_test_image():
    """Factory fixture to create test images."""
    def _create_image(path: Path, colors: list[tuple[int, int, int]] = None, size: tuple[int, int] = (100, 100)):
        """Create a test image with multiple colors.

        Args:
            path: Path to save the image
            colors: List of RGB colors to include. If None, creates a red image.
            size: Image dimensions (width, height)
        """
        if colors is None:
            colors = [(255, 0, 0)]

        img = Image.new("RGB", size)
        pixels = img.load()

        # Divide image into sections for each color
        section_height = size[1] // len(colors)

        for i, color in enumerate(colors):
            y_start = i * section_height
            y_end = size[1] if i == len(
                colors) - 1 else (i + 1) * section_height

            for x in range(size[0]):
                for y in range(y_start, y_end):
                    pixels[x, y] = color

        img.save(path, "JPEG")
    return _create_image


def test_process_images_missing_directory():
    """Test that processing fails when output directory doesn't exist."""
    processor = ImageProcessor()
    nonexistent_dir = Path("/nonexistent/directory")
    # We can't even instantiate FilePaths if the dir doesn't exist
    with pytest.raises(FileNotFoundError):
        FilePaths(nonexistent_dir)


def test_process_images_missing_playlist_json(temp_dir):
    """Test that processing fails when playlist.json is missing."""
    processor = ImageProcessor()
    file_paths = FilePaths(temp_dir)

    with pytest.raises(FileNotFoundError) as exc_info:
        processor.process_playlist(file_paths)

    assert "Playlist file not found" in str(exc_info.value)

    assert "Playlist file not found" in str(exc_info.value)
    assert "get-playlist" in str(exc_info.value)


def test_process_images_missing_image_files(temp_dir, sample_playlist):
    """Test that processing fails when image files are missing."""
    file_paths = FilePaths(temp_dir)
    # Save playlist.json but don't create image files
    playlist_path = file_paths.playlist_path()
    sample_playlist.to_json(playlist_path)

    processor = ImageProcessor()

    with pytest.raises(FileNotFoundError) as exc_info:
        processor.process_playlist(file_paths)

    assert "Missing 3 image file(s)" in str(exc_info.value)
    assert "get-playlist" in str(exc_info.value)


def test_process_images_success(temp_dir, sample_playlist, create_test_image):
    """Test successful image processing with all files present."""
    file_paths = FilePaths(temp_dir)
    # Save playlist.json
    playlist_path = file_paths.playlist_path()
    sample_playlist.to_json(playlist_path)

    # Create test images with multiple colors
    create_test_image(file_paths.track_image_path("track1"),
                      # Red shades
                      colors=[(255, 0, 0), (200, 0, 0), (150, 0, 0)])
    create_test_image(file_paths.track_image_path("track2"),
                      # Green shades
                      colors=[(0, 255, 0), (0, 200, 0), (0, 150, 0)])
    create_test_image(file_paths.track_image_path("track3"),
                      # Blue shades
                      colors=[(0, 0, 255), (0, 0, 200), (0, 0, 150)])

    processor = ImageProcessor()
    results = processor.process_playlist(file_paths, k=3)

    # Verify results
    assert len(results) == 3
    assert all(isinstance(r, ImageColorData) for r in results)

    # Check that all tracks were processed
    track_ids = {r.track_id for r in results}
    assert track_ids == {"track1", "track2", "track3"}

    # Verify no errors
    assert all(r.error is None for r in results)

    # Verify each result has color data (k colors or fewer if image has fewer unique colors)
    for result in results:
        assert len(result.rgbs) >= 1 and len(result.rgbs) <= 3
        assert len(result.hsvs) >= 1 and len(result.hsvs) <= 3
        assert len(result.rgbs) == len(result.hsvs)

        # Verify RGB values are in valid range
        for rgb in result.rgbs:
            assert len(rgb) == 3
            assert all(0 <= val <= 255 for val in rgb)

        # Verify HSV values are in valid range
        for hsv in result.hsvs:
            assert len(hsv) == 3
            h, s, v = hsv
            assert 0 <= h <= 360
            assert 0 <= s <= 100
            assert 0 <= v <= 100


def test_process_images_with_different_k(temp_dir, sample_playlist, create_test_image):
    """Test image processing with different k values."""
    file_paths = FilePaths(temp_dir)
    # Save playlist.json
    playlist_path = file_paths.playlist_path()
    sample_playlist.to_json(playlist_path)

    # Create test images with multiple distinct colors
    create_test_image(file_paths.track_image_path("track1"),
                      colors=[(255, 0, 0), (200, 0, 0), (150, 0, 0), (100, 0, 0), (50, 0, 0)])
    create_test_image(file_paths.track_image_path("track2"),
                      colors=[(0, 255, 0), (0, 200, 0), (0, 150, 0), (0, 100, 0), (0, 50, 0)])
    create_test_image(file_paths.track_image_path("track3"),
                      colors=[(0, 0, 255), (0, 0, 200), (0, 0, 150), (0, 0, 100), (0, 0, 50)])

    processor = ImageProcessor()

    # Test with k=1
    results_k1 = processor.process_playlist(file_paths, k=1)
    assert all(len(r.rgbs) == 1 for r in results_k1)
    assert all(len(r.hsvs) == 1 for r in results_k1)

    # Test with k=5
    results_k5 = processor.process_playlist(file_paths, k=5)
    # Note: k-means may return fewer clusters if there aren't enough distinct colors
    assert all(len(r.rgbs) >= 1 and len(r.rgbs) <= 5 for r in results_k5)
    assert all(len(r.hsvs) >= 1 and len(r.hsvs) <= 5 for r in results_k5)


def test_process_images_with_corrupted_image(temp_dir, sample_playlist, create_test_image):
    """Test that corrupted images are flagged but processing continues."""
    file_paths = FilePaths(temp_dir)
    # Save playlist.json
    playlist_path = file_paths.playlist_path()
    sample_playlist.to_json(playlist_path)

    # Create valid images for track1 and track3
    create_test_image(file_paths.track_image_path("track1"),
                      colors=[(255, 0, 0), (200, 0, 0), (150, 0, 0)])
    create_test_image(file_paths.track_image_path("track3"),
                      colors=[(0, 0, 255), (0, 0, 200), (0, 0, 150)])

    # Create corrupted image for track2
    corrupted_path = file_paths.track_image_path("track2")
    with open(corrupted_path, "w") as f:
        f.write("This is not a valid JPEG file")

    processor = ImageProcessor()
    results = processor.process_playlist(file_paths, k=3)

    # Verify all tracks are in results
    assert len(results) == 3

    # Check track2 has an error
    track2_result = next(r for r in results if r.track_id == "track2")
    assert track2_result.error is not None
    assert len(track2_result.rgbs) == 0
    assert len(track2_result.hsvs) == 0

    # Check track1 and track3 processed successfully
    track1_result = next(r for r in results if r.track_id == "track1")
    track3_result = next(r for r in results if r.track_id == "track3")

    assert track1_result.error is None
    assert len(track1_result.rgbs) >= 1
    assert len(track1_result.hsvs) >= 1

    assert track3_result.error is None
    assert len(track3_result.rgbs) >= 1
    assert len(track3_result.hsvs) >= 1


def test_image_color_data_serialization():
    """Test ImageColorData to_dict and from_dict methods."""
    data = ImageColorData(
        track_id="test_track",
        rgbs=[(255, 0, 0), (0, 255, 0), (0, 0, 255)],
        hsvs=[(0.0, 100.0, 100.0), (120.0, 100.0, 100.0), (240.0, 100.0, 100.0)],
        error=None,
    )

    # Test to_dict
    data_dict = data.to_dict()
    assert data_dict["track_id"] == "test_track"
    assert data_dict["rgbs"] == [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    assert data_dict["error"] is None

    # Test from_dict
    restored = ImageColorData.from_dict(data_dict)
    assert restored.track_id == data.track_id
    assert restored.rgbs == data.rgbs
    assert restored.hsvs == data.hsvs
    assert restored.error == data.error


def test_image_color_data_serialization_with_error():
    """Test ImageColorData serialization when error is present."""
    data = ImageColorData(
        track_id="test_track",
        rgbs=[],
        hsvs=[],
        error="Failed to process image",
    )

    data_dict = data.to_dict()
    assert data_dict["error"] == "Failed to process image"
    assert data_dict["rgbs"] == []
    assert data_dict["hsvs"] == []

    restored = ImageColorData.from_dict(data_dict)
    assert restored.error == "Failed to process image"
    assert restored.rgbs == []
    assert restored.hsvs == []


def test_extract_colors_sorts_by_frequency(temp_dir, create_test_image):
    """Test that extracted colors are sorted by frequency (most common first)."""
    # Create an image with mostly red pixels and some blue pixels
    img = Image.new("RGB", (100, 100))
    pixels = img.load()

    # Fill most of the image with red
    for x in range(100):
        for y in range(80):
            pixels[x, y] = (255, 0, 0)

    # Fill bottom part with blue
    for x in range(100):
        for y in range(80, 100):
            pixels[x, y] = (0, 0, 255)

    image_path = temp_dir / "test.jpg"
    img.save(image_path, "JPEG")

    processor = ImageProcessor()
    rgbs, hsvs = processor.extract_colors(image_path, k=2)

    # The most frequent color (red) should be first
    # Note: Due to JPEG compression, colors might not be exact
    assert len(rgbs) == 2
    assert len(hsvs) == 2

    # First color should be more red-ish (higher R component)
    assert rgbs[0][0] > rgbs[1][0]  # Red component of first should be higher
