# SPDX-License-Identifier: Apache-2.0
# Copyright (2026) Beachgeek.co.uk
# Author: Ricardo Sueiras
# Apache 2.0 license

"""Routes package."""

from src.routes.auth import auth_bp
from src.routes.surveys import surveys_bp
from src.routes.pages import pages_bp

__all__ = ["auth_bp", "surveys_bp", "pages_bp"]
