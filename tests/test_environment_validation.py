"""Tests for environment variable validation."""
import os
from unittest.mock import patch

import pytest


def test_validate_environment_all_vars_present():
    """Test that validation passes when all required env vars are set."""
    from chromalist.__main__ import validate_environment

    with patch.dict(os.environ, {
        "SPOTIPY_CLIENT_ID": "test_client_id",
        "SPOTIPY_CLIENT_SECRET": "test_client_secret",
        "SPOTIPY_REDIRECT_URI": "http://localhost:3000/callback",
    }):
        # Should not raise any exception
        validate_environment()


def test_validate_environment_missing_client_id():
    """Test that validation fails when SPOTIPY_CLIENT_ID is missing."""
    from chromalist.__main__ import validate_environment

    with patch.dict(os.environ, {
        "SPOTIPY_CLIENT_SECRET": "test_client_secret",
        "SPOTIPY_REDIRECT_URI": "http://localhost:3000/callback",
    }, clear=True):
        with pytest.raises(SystemExit) as exc_info:
            validate_environment()
        assert exc_info.value.code == 1


def test_validate_environment_missing_client_secret():
    """Test that validation fails when SPOTIPY_CLIENT_SECRET is missing."""
    from chromalist.__main__ import validate_environment

    with patch.dict(os.environ, {
        "SPOTIPY_CLIENT_ID": "test_client_id",
        "SPOTIPY_REDIRECT_URI": "http://localhost:3000/callback",
    }, clear=True):
        with pytest.raises(SystemExit) as exc_info:
            validate_environment()
        assert exc_info.value.code == 1


def test_validate_environment_missing_redirect_uri():
    """Test that validation fails when SPOTIPY_REDIRECT_URI is missing."""
    from chromalist.__main__ import validate_environment

    with patch.dict(os.environ, {
        "SPOTIPY_CLIENT_ID": "test_client_id",
        "SPOTIPY_CLIENT_SECRET": "test_client_secret",
    }, clear=True):
        with pytest.raises(SystemExit) as exc_info:
            validate_environment()
        assert exc_info.value.code == 1


def test_validate_environment_missing_all_vars():
    """Test that validation fails when all env vars are missing."""
    from chromalist.__main__ import validate_environment

    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(SystemExit) as exc_info:
            validate_environment()
        assert exc_info.value.code == 1


def test_validate_environment_error_message_content(capsys):
    """Test that error message contains helpful setup instructions."""
    from chromalist.__main__ import validate_environment

    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(SystemExit):
            validate_environment()

        captured = capsys.readouterr()
        error_output = captured.err

        # Check for key elements in error message
        assert "ERROR" in error_output
        assert "SPOTIPY_CLIENT_ID" in error_output
        assert "SPOTIPY_CLIENT_SECRET" in error_output
        assert "SPOTIPY_REDIRECT_URI" in error_output
        assert "Setup Instructions" in error_output
        assert "developer.spotify.com" in error_output
