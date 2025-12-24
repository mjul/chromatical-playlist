# Use a standard Microsoft Python dev container base
# https://hub.docker.com/r/microsoft/devcontainers-python
FROM mcr.microsoft.com/devcontainers/python:1-3.12-bookworm

# Install uv by copying the binary from the official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set uv environment variables
ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=auto

# Ensure the 'vscode' user has access to the binaries
RUN chown vscode:vscode /bin/uv /bin/uvx

USER vscode
