# SPDX-License-Identifier: Apache-2.0
# Copyright (2026) Beachgeek.co.uk
# Author: Ricardo Sueiras
# Apache 2.0 license

FROM python:3.12-slim AS builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies to virtual environment
RUN uv sync --frozen --no-dev

FROM python:3.12-slim

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

# Copy application code
COPY . .

# Create non-root user and set permissions
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app && \
    chmod +x entrypoint.sh

USER appuser

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

ENTRYPOINT ["./entrypoint.sh"]
