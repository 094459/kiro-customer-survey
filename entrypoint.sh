#!/bin/bash
# SPDX-License-Identifier: Apache-2.0
# Copyright (2026) Beachgeek.co.uk
# Author: Ricardo Sueiras
# Apache 2.0 license

set -e

# Initialize database if it doesn't exist
if [ ! -f "/app/survey.db" ]; then
    echo "Initializing database..."
    python -c "from src import create_app; from src.extensions import db; app = create_app(); app.app_context().push(); db.create_all()"
fi

# Start Gunicorn
exec gunicorn -c gunicorn.conf.py run:app
