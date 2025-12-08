# SPDX-License-Identifier: Apache-2.0
# Copyright (2026) Beachgeek.co.uk
# Author: Ricardo Sueiras
# Apache 2.0 license

"""Application entry point."""

from src import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
