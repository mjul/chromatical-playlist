import os
import sys

from chromalist.cli import app


def validate_environment() -> None:
    """Validate that required Spotify environment variables are set.

    Raises:
        SystemExit: If required environment variables are missing.
    """
    required_vars = [
        "SPOTIPY_CLIENT_ID",
        "SPOTIPY_CLIENT_SECRET",
        "SPOTIPY_REDIRECT_URI",
    ]

    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        print(
            "\n❌ ERROR: Missing required Spotify environment variables:\n", file=sys.stderr)
        for var in missing_vars:
            print(f"  - {var}", file=sys.stderr)

        print("\n📚 Setup Instructions:", file=sys.stderr)
        print("  1. Create a Spotify application at: https://developer.spotify.com/dashboard", file=sys.stderr)
        print("  2. Set the following environment variables:", file=sys.stderr)
        print("     export SPOTIPY_CLIENT_ID='your_client_id'", file=sys.stderr)
        print("     export SPOTIPY_CLIENT_SECRET='your_client_secret'", file=sys.stderr)
        print("     export SPOTIPY_REDIRECT_URI='https://127.0.0.1:3000/callback'", file=sys.stderr)
        print(
            "\n  Alternatively, create a .env file with these variables.\n", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    validate_environment()
    app()
