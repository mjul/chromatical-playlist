from pathlib import Path

import typer
from typing_extensions import Annotated

from chromalist.files import FilePaths
from chromalist.image_processing import ImageProcessor
from chromalist.spotify_client import SpotifyClient

app = typer.Typer()

# Global option for output directory
output_dir_option = Annotated[
    Path,
    typer.Option(
        "--output-dir",
        "-o",
        help="Directory to store intermediate files (playlists, images, etc.)",
    ),
]


@app.command()
def get_playlist(
    playlist_id: Annotated[str, typer.Argument(help="Spotify playlist ID or URI")],
    output_dir: output_dir_option = Path("tmp"),
) -> None:
    """Download a playlist and its album cover images from Spotify.

    Downloads playlist metadata to playlist.json and album covers as {track-id}.jpg
    in the output directory.
    """
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    file_paths = FilePaths(output_dir)

    typer.echo(f"📡 Fetching playlist: {playlist_id}")

    # Initialize Spotify client and fetch playlist
    try:
        client = SpotifyClient()
        playlist = client.get_playlist(playlist_id)
    except Exception as e:
        typer.echo(f"❌ Error fetching playlist: {e}", err=True)
        raise typer.Exit(code=1)

    typer.echo(
        f"✅ Found playlist: '{playlist.name}' with {len(playlist.tracks)} tracks")

    # Save playlist metadata
    playlist_file = file_paths.playlist_path()
    playlist.to_json(playlist_file)
    typer.echo(f"💾 Saved playlist metadata to {playlist_file}")

    # Download album art for each track
    typer.echo("\n🖼️  Downloading album cover art...")

    with typer.progressbar(playlist.tracks, label="Downloading") as progress:
        for track in progress:
            if track.album_art_url:
                try:
                    client.download_album_art(
                        track.id, track.album_art_url, file_paths)
                except Exception as e:
                    typer.echo(
                        f"\n⚠️  Warning: Failed to download art for '{track.name}': {e}", err=True)

    typer.echo(
        f"\n✅ Done! Downloaded {len(playlist.tracks)} album covers to {output_dir}")


@app.command()
def process_images(
    output_dir: output_dir_option = Path("tmp"),
    k: Annotated[int, typer.Option(
        help="Number of dominant colours to extract per image")] = 3,
) -> None:
    """Process images to extract dominant colours.

    Reads images from output directory and writes colour data to image-colours.json.
    """
    import json

    typer.echo(f"🔮 Processing images in {output_dir}...")

    # Validate output directory exists
    if not output_dir.exists():
        typer.echo(
            f"❌ Error: Output directory does not exist: {output_dir}", err=True)
        typer.echo(
            "Please run 'get-playlist' first to download playlist data.", err=True)
        raise typer.Exit(code=1)

    file_paths = FilePaths(output_dir)

    # Process images
    try:
        processor = ImageProcessor()
        results = processor.process_playlist(file_paths, k=k)
    except FileNotFoundError as e:
        typer.echo(f"❌ Error: {e}", err=True)
        raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"❌ Error processing images: {e}", err=True)
        raise typer.Exit(code=1)

    # Count errors
    error_count = sum(1 for r in results if r.error is not None)
    success_count = len(results) - error_count

    typer.echo(
        f"✅ Successfully processed {success_count}/{len(results)} images")
    if error_count > 0:
        typer.echo(
            f"⚠️  {error_count} image(s) had processing errors (see image-colours.json)")

    # Save results to JSON
    output_file = file_paths.image_colours_path()
    try:
        with open(output_file, "w") as f:
            json.dump([r.to_dict() for r in results], f, indent=2)
        typer.echo(f"💾 Saved colour data to {output_file}")
    except Exception as e:
        typer.echo(f"❌ Error saving results to {output_file}: {e}", err=True)
        raise typer.Exit(code=1)


@app.command()
def generate_sorted_playlist(
    output_dir: output_dir_option = Path("tmp"),
) -> None:
    """Generate a chromatically sorted playlist.

    Reads playlist.json and image-colours.json from output directory,
    sorts tracks by the hue of their dominant album cover colour,
    and writes sorted-playlist.json.
    """
    from chromalist.playlist_sorting import sort_playlist_by_hue

    typer.echo(f"🎨 Generating sorted playlist from {output_dir}...")

    # Validate output directory exists
    if not output_dir.exists():
        typer.echo(
            f"❌ Error: Output directory does not exist: {output_dir}", err=True
        )
        typer.echo(
            "Please run 'get-playlist' and 'process-images' first.", err=True
        )
        raise typer.Exit(code=1)

    file_paths = FilePaths(output_dir)

    try:
        sorted_playlist, excluded_count = sort_playlist_by_hue(file_paths)

        typer.echo(f"✅ Sorted {len(sorted_playlist.tracks)} tracks by hue")

        if excluded_count > 0:
            typer.echo(
                f"⚠️  Excluded {excluded_count} track(s) without valid colour data"
            )

        output_file = file_paths.sorted_playlist_path()
        typer.echo(f"💾 Saved sorted playlist to {output_file}")

    except FileNotFoundError as e:
        typer.echo(f"❌ Error: {e}", err=True)
        raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"❌ Error generating sorted playlist: {e}", err=True)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
