# SPDX-License-Identifier: Apache-2.0
# Copyright (2026) Beachgeek.co.uk
# Author: Ricardo Sueiras
# Apache 2.0 license

"""Pytest configuration and fixtures."""

import pytest
from src import create_app
from src.extensions import db
from src.models import User, Survey, SurveyOption
from werkzeug.security import generate_password_hash


@pytest.fixture
def app():
    """Create test app with in-memory database."""
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["WTF_CSRF_ENABLED"] = False
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def test_user(app):
    """Create test user."""
    with app.app_context():
        user = User(
            email="test@example.com",
            password_hash=generate_password_hash("password123")
        )
        db.session.add(user)
        db.session.commit()
        return user.id


@pytest.fixture
def authenticated_client(client, test_user):
    """Create authenticated test client."""
    client.post("/login", data={
        "email": "test@example.com",
        "password": "password123"
    })
    return client


@pytest.fixture
def test_survey(app, test_user):
    """Create test survey with options."""
    with app.app_context():
        survey = Survey(
            user_id=test_user,
            title="Test Survey",
            description="Test Description",
            is_active=True
        )
        db.session.add(survey)
        db.session.flush()
        
        for i in range(1, 4):
            option = SurveyOption(
                survey_id=survey.id,
                option_text=f"Option {i}",
                option_order=i
            )
            db.session.add(option)
        
        db.session.commit()
        return survey.id
