from pathlib import Path

import typer
from typing_extensions import Annotated

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
    playlist_file = output_dir / "playlist.json"
    playlist.to_json(str(playlist_file))
    typer.echo(f"💾 Saved playlist metadata to {playlist_file}")

    # Download album art for each track
    typer.echo("\n🖼️  Downloading album cover art...")

    with typer.progressbar(playlist.tracks, label="Downloading") as progress:
        for track in progress:
            if track.album_art_url:
                try:
                    client.download_album_art(
                        track.id, track.album_art_url, output_dir)
                except Exception as e:
                    typer.echo(
                        f"\n⚠️  Warning: Failed to download art for '{track.name}': {e}", err=True)

    typer.echo(
        f"\n✅ Done! Downloaded {len(playlist.tracks)} album covers to {output_dir}")


@app.command()
def process_images(
    output_dir: output_dir_option = Path("tmp"),
) -> None:
    """Process images to extract dominant colors (NOT YET IMPLEMENTED).

    Reads images from output directory and writes color data to image-colours.json.
    """
    typer.echo(f"🔮 Processing images in {output_dir}...")
    typer.echo("⚠️  This command is not yet implemented.")
    raise typer.Exit(code=1)


@app.command()
def generate_sorted_playlist(
    output_dir: output_dir_option = Path("tmp"),
) -> None:
    """Generate a chromatically sorted playlist (NOT YET IMPLEMENTED).

    Reads playlist.json and image-colours.json from output directory and
    generates sorted-playlist.json.
    """
    typer.echo(f"🎨 Generating sorted playlist from {output_dir}...")
    typer.echo("⚠️  This command is not yet implemented.")
    raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
