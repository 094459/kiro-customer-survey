# SPDX-License-Identifier: Apache-2.0
# Copyright (2026) Beachgeek.co.uk
# Author: Ricardo Sueiras
# Apache 2.0 license

"""Tests for authentication routes."""

from src.models import User
from src.extensions import db


def test_register_get(client):
    """Test register page loads."""
    response = client.get("/register")
    assert response.status_code == 200
    assert b"Register" in response.data


def test_register_success(client, app):
    """Test successful registration."""
    response = client.post("/register", data={
        "email": "newuser@test.com",
        "password": "password123"
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b"Registration successful" in response.data
    
    with app.app_context():
        user = User.query.filter_by(email="newuser@test.com").first()
        assert user is not None


def test_register_duplicate_email(client, test_user):
    """Test registration with duplicate email."""
    response = client.post("/register", data={
        "email": "test@example.com",
        "password": "password123"
    })
    
    assert b"Email already registered" in response.data


def test_register_missing_fields(client):
    """Test registration with missing fields."""
    response = client.post("/register", data={
        "email": "",
        "password": ""
    })
    
    assert b"Email and password are required" in response.data


def test_login_get(client):
    """Test login page loads."""
    response = client.get("/login")
    assert response.status_code == 200
    assert b"Login" in response.data


def test_login_success(client, test_user):
    """Test successful login."""
    response = client.post("/login", data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b"Dashboard" in response.data


def test_login_invalid_credentials(client, test_user):
    """Test login with invalid credentials."""
    response = client.post("/login", data={
        "email": "test@example.com",
        "password": "wrongpassword"
    })
    
    assert b"Invalid email or password" in response.data


def test_login_nonexistent_user(client):
    """Test login with nonexistent user."""
    response = client.post("/login", data={
        "email": "nonexistent@test.com",
        "password": "password123"
    })
    
    assert b"Invalid email or password" in response.data


def test_logout(authenticated_client):
    """Test logout."""
    response = authenticated_client.get("/logout", follow_redirects=True)
    
    assert response.status_code == 200
    assert b"Login" in response.data


def test_protected_route_requires_auth(client):
    """Test protected route redirects to login."""
    response = client.get("/dashboard")
    assert response.status_code == 302
    assert "/login" in response.location
