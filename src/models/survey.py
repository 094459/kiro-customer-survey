# SPDX-License-Identifier: Apache-2.0
# Copyright (2026) Beachgeek.co.uk
# Author: Ricardo Sueiras
# Apache 2.0 license

"""Survey models."""

from datetime import datetime
from src.extensions import db


class Survey(db.Model):
    __tablename__ = "surveys"
    
    id = db.Column("survey_id", db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = db.relationship("User", back_populates="surveys")
    options = db.relationship("SurveyOption", back_populates="survey", cascade="all, delete-orphan")
    responses = db.relationship("SurveyResponse", back_populates="survey", cascade="all, delete-orphan")


class SurveyOption(db.Model):
    __tablename__ = "survey_options"
    
    id = db.Column("option_id", db.Integer, primary_key=True)
    survey_id = db.Column(db.Integer, db.ForeignKey("surveys.survey_id"), nullable=False)
    option_text = db.Column(db.String(255), nullable=False)
    option_order = db.Column(db.Integer, nullable=False)
    
    survey = db.relationship("Survey", back_populates="options")
    responses = db.relationship("SurveyResponse", back_populates="option", cascade="all, delete-orphan")


class SurveyResponse(db.Model):
    __tablename__ = "survey_responses"
    
    id = db.Column("response_id", db.Integer, primary_key=True)
    survey_id = db.Column(db.Integer, db.ForeignKey("surveys.survey_id"), nullable=False)
    option_id = db.Column(db.Integer, db.ForeignKey("survey_options.option_id"), nullable=False)
    respondent_email = db.Column(db.String(255))
    response_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    survey = db.relationship("Survey", back_populates="responses")
    option = db.relationship("SurveyOption", back_populates="responses")
