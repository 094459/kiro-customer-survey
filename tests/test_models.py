# SPDX-License-Identifier: Apache-2.0
# Copyright (2026) Beachgeek.co.uk
# Author: Ricardo Sueiras
# Apache 2.0 license

"""Tests for models."""

from src.models import User, Survey, SurveyOption, SurveyResponse
from src.extensions import db


def test_user_creation(app):
    """Test user model creation."""
    with app.app_context():
        user = User(email="user@test.com", password_hash="hashed")
        db.session.add(user)
        db.session.commit()
        
        assert user.id is not None
        assert user.email == "user@test.com"
        assert user.created_at is not None


def test_user_relationships(app, test_user):
    """Test user relationships."""
    with app.app_context():
        user = User.query.get(test_user)
        survey = Survey(user_id=user.id, title="Test")
        db.session.add(survey)
        db.session.commit()
        
        assert len(user.surveys) == 1
        assert user.surveys[0].title == "Test"


def test_survey_creation(app, test_user):
    """Test survey model creation."""
    with app.app_context():
        survey = Survey(
            user_id=test_user,
            title="Survey Title",
            description="Description"
        )
        db.session.add(survey)
        db.session.commit()
        
        assert survey.id is not None
        assert survey.title == "Survey Title"
        assert survey.is_active is True


def test_survey_option_creation(app, test_survey):
    """Test survey option creation."""
    with app.app_context():
        options = SurveyOption.query.filter_by(survey_id=test_survey).all()
        
        assert len(options) == 3
        assert options[0].option_text == "Option 1"
        assert options[0].option_order == 1


def test_survey_response_creation(app, test_survey):
    """Test survey response creation."""
    with app.app_context():
        option = SurveyOption.query.filter_by(survey_id=test_survey).first()
        response = SurveyResponse(
            survey_id=test_survey,
            option_id=option.id,
            respondent_email="respondent@test.com"
        )
        db.session.add(response)
        db.session.commit()
        
        assert response.id is not None
        assert response.respondent_email == "respondent@test.com"


def test_cascade_delete(app, test_user):
    """Test cascade delete on survey deletion."""
    with app.app_context():
        survey = Survey(user_id=test_user, title="Delete Test")
        db.session.add(survey)
        db.session.flush()
        
        option = SurveyOption(
            survey_id=survey.id,
            option_text="Option",
            option_order=1
        )
        db.session.add(option)
        db.session.commit()
        
        survey_id = survey.id
        db.session.delete(survey)
        db.session.commit()
        
        assert SurveyOption.query.filter_by(survey_id=survey_id).count() == 0
