# Testing Guide

## Running Tests

All tests use pytest with mocked Spotify API calls, so they don't require actual Spotify credentials.

### Run all tests
```bash
uv run pytest
```

### Run specific test files
```bash
# Test environment validation
uv run pytest tests/test_environment_validation.py -v

# Test Spotify client
uv run pytest tests/test_spotify_client.py -v
```

### Run tests with coverage
```bash
uv run pytest --cov=chromalist --cov-report=html
```

## Manual Testing

### 1. Test Environment Validation

Running the application without environment variables should fail with a helpful error message:

```bash
uv run python -m chromalist --help
```

Expected output:
```
❌ ERROR: Missing required Spotify environment variables:

  - SPOTIPY_CLIENT_ID
  - SPOTIPY_CLIENT_SECRET
  - SPOTIPY_REDIRECT_URI

📚 Setup Instructions:
  1. Create a Spotify application at: https://developer.spotify.com/dashboard
  2. Set the following environment variables:
     export SPOTIPY_CLIENT_ID='your_client_id'
     export SPOTIPY_CLIENT_SECRET='your_client_secret'
     export SPOTIPY_REDIRECT_URI='https://127.0.0.1:3000/callback'

  Alternatively, create a .env file with these variables.
```

### 2. Setup Spotify Credentials

1. Go to https://developer.spotify.com/dashboard
2. Create a new application
3. Copy the Client ID and Client Secret
4. Create a `.env` file:

```bash
cp .env.example .env
# Edit .env with your actual credentials
```

Or export environment variables:
```bash
export SPOTIPY_CLIENT_ID='your_actual_client_id'
export SPOTIPY_CLIENT_SECRET='your_actual_client_secret'
export SPOTIPY_REDIRECT_URI='https://127.0.0.1:3000/callback'
```

### 3. Test Playlist Download

With valid credentials, you can download a public Spotify playlist:

```bash
# Example with a public playlist (replace with any Spotify playlist ID)
uv run python -m chromalist get-playlist 37i9dQZF1DXcBWIGoYBM5M

# Or specify a custom output directory
uv run python -m chromalist get-playlist 37i9dQZF1DXcBWIGoYBM5M --output-dir my-playlists
```

This will:
1. Authenticate with Spotify (opens browser for first-time OAuth)
2. Fetch the playlist metadata
3. Save `playlist.json` to the output directory
4. Download all album cover images as `{track-id}.jpg`

### 4. Verify Output

After successful download, check the output directory:

```bash
ls -la tmp/
# Should contain:
# - playlist.json (playlist metadata)
# - {track-id}.jpg files (album covers)
```

Inspect the playlist JSON:
```bash
cat tmp/playlist.json | python -m json.tool | head -50
```

## Test Playlists

Some public Spotify playlists you can use for testing:

- **Today's Top Hits**: `37i9dQZF1DXcBWIGoYBM5M`
- **RapCaviar**: `37i9dQZF1DX0XUsuxWHRQd`
- **Rock Classics**: `37i9dQZF1DWXRqgorJj26U`

## Troubleshooting

### OAuth Issues

If you get OAuth errors:
1. Make sure the Redirect URI in your Spotify app settings matches `SPOTIPY_REDIRECT_URI`
2. Clear cached credentials: `rm -rf .cache*`
3. Try again

### Network Issues

If downloads fail:
- Check your internet connection
- Some tracks may have unavailable album art (these are skipped with a warning)
- Try a smaller playlist first

### Permission Errors

If you get file permission errors:
- Make sure the output directory is writable
- Try a different output directory with `--output-dir`
