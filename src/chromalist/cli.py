import typer

app = typer.Typer()

@app.command()
def sort(playlist_id: str):
    """
    Sort a Spotify playlist chromatographically.
    """
    typer.echo(f"Sorting playlist: {playlist_id}")

if __name__ == "__main__":
    app()
