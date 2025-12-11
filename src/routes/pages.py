# SPDX-License-Identifier: Apache-2.0
# Copyright (2026) Beachgeek.co.uk
# Author: Ricardo Sueiras
# Apache 2.0 license

"""Static pages routes."""

from flask import Blueprint, render_template

pages_bp = Blueprint("pages", __name__)


@pages_bp.route("/help")
def help_page():
    """Display help page."""
    return render_template("help.html")


@pages_bp.route("/contact")
def contact_page():
    """Display contact us page."""
    return render_template("contact.html")
