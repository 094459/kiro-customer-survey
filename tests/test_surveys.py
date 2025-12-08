# SPDX-License-Identifier: Apache-2.0
# Copyright (2026) Beachgeek.co.uk
# Author: Ricardo Sueiras
# Apache 2.0 license

"""Tests for survey routes."""

from src.models import Survey, SurveyOption, SurveyResponse
from src.extensions import db


def test_dashboard_requires_auth(client):
    """Test dashboard requires authentication."""
    response = client.get("/dashboard")
    assert response.status_code == 302


def test_dashboard_shows_surveys(authenticated_client, test_survey):
    """Test dashboard displays user surveys."""
    response = authenticated_client.get("/dashboard")
    assert response.status_code == 200
    assert b"Test Survey" in response.data


def test_create_survey_get(authenticated_client):
    """Test create survey page loads."""
    response = authenticated_client.get("/survey/create")
    assert response.status_code == 200
    assert b"Create New Survey" in response.data


def test_create_survey_success(authenticated_client, app):
    """Test successful survey creation."""
    response = authenticated_client.post("/survey/create", data={
        "title": "New Survey",
        "description": "Description",
        "option_1": "Option 1",
        "option_2": "Option 2"
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b"Survey created successfully" in response.data
    
    with app.app_context():
        survey = Survey.query.filter_by(title="New Survey").first()
        assert survey is not None
        assert len(survey.options) == 2


def test_create_survey_missing_title(authenticated_client):
    """Test survey creation without title."""
    response = authenticated_client.post("/survey/create", data={
        "title": "",
        "option_1": "Option 1",
        "option_2": "Option 2"
    })
    
    assert b"Title is required" in response.data


def test_create_survey_insufficient_options(authenticated_client):
    """Test survey creation with less than 2 options."""
    response = authenticated_client.post("/survey/create", data={
        "title": "Survey",
        "option_1": "Option 1"
    })
    
    assert b"At least 2 options are required" in response.data


def test_create_survey_max_options(authenticated_client, app):
    """Test survey creation with 5 options."""
    response = authenticated_client.post("/survey/create", data={
        "title": "Max Options Survey",
        "option_1": "Option 1",
        "option_2": "Option 2",
        "option_3": "Option 3",
        "option_4": "Option 4",
        "option_5": "Option 5"
    }, follow_redirects=True)
    
    assert response.status_code == 200
    
    with app.app_context():
        survey = Survey.query.filter_by(title="Max Options Survey").first()
        assert len(survey.options) == 5


def test_toggle_survey(authenticated_client, app, test_survey):
    """Test toggling survey active status."""
    response = authenticated_client.get(
        f"/survey/{test_survey}/toggle",
        follow_redirects=True
    )
    
    assert response.status_code == 200
    
    with app.app_context():
        survey = Survey.query.get(test_survey)
        assert survey.is_active is False


def test_toggle_nonexistent_survey(authenticated_client):
    """Test toggling nonexistent survey."""
    response = authenticated_client.get("/survey/9999/toggle", follow_redirects=True)
    assert b"Survey not found" in response.data


def test_survey_response_get(client, test_survey):
    """Test public survey response page."""
    response = client.get(f"/s/{test_survey}")
    assert response.status_code == 200
    assert b"Test Survey" in response.data
    assert b"Option 1" in response.data


def test_survey_response_inactive(client, app, test_survey):
    """Test accessing inactive survey."""
    with app.app_context():
        survey = Survey.query.get(test_survey)
        survey.is_active = False
        db.session.commit()
    
    response = client.get(f"/s/{test_survey}")
    assert response.status_code == 404


def test_survey_response_submit(client, app, test_survey):
    """Test submitting survey response."""
    with app.app_context():
        option = SurveyOption.query.filter_by(survey_id=test_survey).first()
        option_id = option.id
    
    response = client.post(f"/s/{test_survey}", data={
        "option_id": option_id,
        "email": "respondent@test.com"
    })
    
    assert response.status_code == 200
    assert b"Thank You" in response.data
    
    with app.app_context():
        responses = SurveyResponse.query.filter_by(survey_id=test_survey).all()
        assert len(responses) == 1
        assert responses[0].respondent_email == "respondent@test.com"


def test_survey_response_no_option(client, test_survey):
    """Test submitting response without selecting option."""
    response = client.post(f"/s/{test_survey}", data={
        "email": "test@test.com"
    })
    
    assert b"Please select an option" in response.data


def test_survey_results_requires_auth(client, test_survey):
    """Test results page requires authentication."""
    response = client.get(f"/survey/{test_survey}/results")
    assert response.status_code == 302


def test_survey_results(authenticated_client, app, test_survey):
    """Test viewing survey results."""
    with app.app_context():
        option = SurveyOption.query.filter_by(survey_id=test_survey).first()
        response = SurveyResponse(
            survey_id=test_survey,
            option_id=option.id
        )
        db.session.add(response)
        db.session.commit()
    
    response = authenticated_client.get(f"/survey/{test_survey}/results")
    assert response.status_code == 200
    assert b"Results" in response.data
    assert b"1 total responses" in response.data


def test_survey_results_unauthorized(client, app, test_user, test_survey):
    """Test viewing results of another user's survey."""
    with app.app_context():
        from src.models import User
        from werkzeug.security import generate_password_hash
        
        other_user = User(
            email="other@test.com",
            password_hash=generate_password_hash("password")
        )
        db.session.add(other_user)
        db.session.commit()
    
    client.post("/login", data={
        "email": "other@test.com",
        "password": "password"
    })
    
    response = client.get(f"/survey/{test_survey}/results", follow_redirects=True)
    assert b"Survey not found" in response.data


def test_root_redirect_authenticated(authenticated_client):
    """Test root redirects to dashboard when authenticated."""
    response = authenticated_client.get("/", follow_redirects=False)
    assert response.status_code == 302
    assert "/dashboard" in response.location


def test_root_redirect_unauthenticated(client):
    """Test root redirects to login when not authenticated."""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.location
