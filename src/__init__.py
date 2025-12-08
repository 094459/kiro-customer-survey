# SPDX-License-Identifier: Apache-2.0
# Copyright (2026) Beachgeek.co.uk
# Author: Ricardo Sueiras
# Apache 2.0 license

"""Flask application factory."""

import os
from pathlib import Path
from flask import Flask, redirect, url_for
from flask_login import current_user
from dotenv import load_dotenv
from src.extensions import db, login_manager, csrf

load_dotenv()


def create_app() -> Flask:
    """Create and configure Flask application."""
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static"
    )
    
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")
    db_path = Path(os.getenv("DATABASE_PATH", "survey.db"))
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path.absolute()}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    
    @login_manager.user_loader
    def load_user(user_id: str):
        from src.models import User
        return User.query.get(int(user_id))
    
    from src.routes import auth_bp, surveys_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(surveys_bp)
    
    @app.route("/")
    def index():
        if current_user.is_authenticated:
            return redirect(url_for("surveys.dashboard"))
        return redirect(url_for("auth.login"))
    
    with app.app_context():
        db.create_all()
    
    return app
