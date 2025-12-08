# SPDX-License-Identifier: Apache-2.0
# Copyright (2026) Beachgeek.co.uk
# Author: Ricardo Sueiras
# Apache 2.0 license

"""Authentication routes."""

from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, Response
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from src.extensions import db
from src.models import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register() -> str | Response:
    """User registration."""
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        
        if not email or not password:
            flash("Email and password are required")
            return render_template("register.html")
        
        if User.query.filter_by(email=email).first():
            flash("Email already registered")
            return render_template("register.html")
        
        user = User(
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        
        flash("Registration successful! Please login.")
        return redirect(url_for("auth.login"))
    
    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login() -> str | Response:
    """User login."""
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            user.last_login = datetime.utcnow()
            db.session.commit()
            login_user(user)
            return redirect(url_for("surveys.dashboard"))
        
        flash("Invalid email or password")
    
    return render_template("login.html")


@auth_bp.route("/logout")
def logout() -> Response:
    """User logout."""
    logout_user()
    return redirect(url_for("auth.login"))
