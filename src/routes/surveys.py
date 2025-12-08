# SPDX-License-Identifier: Apache-2.0
# Copyright (2026) Beachgeek.co.uk
# Author: Ricardo Sueiras
# Apache 2.0 license

"""Survey routes."""

from flask import Blueprint, render_template, request, redirect, url_for, flash, Response
from flask_login import login_required, current_user
from sqlalchemy import func
from src.extensions import db
from src.models import Survey, SurveyOption, SurveyResponse

surveys_bp = Blueprint("surveys", __name__)


@surveys_bp.route("/dashboard")
@login_required
def dashboard() -> str:
    """User dashboard."""
    surveys = Survey.query.filter_by(user_id=current_user.id).order_by(Survey.created_at.desc()).all()
    return render_template("dashboard.html", surveys=surveys)


@surveys_bp.route("/survey/create", methods=["GET", "POST"])
@login_required
def create_survey() -> str | Response:
    """Create new survey."""
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        options = [
            request.form.get(f"option_{i}", "").strip() 
            for i in range(1, 6)
        ]
        options = [opt for opt in options if opt]
        
        if not title:
            flash("Title is required")
            return render_template("create_survey.html")
        
        if len(options) < 2:
            flash("At least 2 options are required")
            return render_template("create_survey.html")
        
        survey = Survey(user_id=current_user.id, title=title, description=description)
        db.session.add(survey)
        db.session.flush()
        
        for idx, option_text in enumerate(options, 1):
            option = SurveyOption(
                survey_id=survey.id,
                option_text=option_text,
                option_order=idx
            )
            db.session.add(option)
        
        db.session.commit()
        flash("Survey created successfully!")
        return redirect(url_for("surveys.dashboard"))
    
    return render_template("create_survey.html")


@surveys_bp.route("/survey/<int:survey_id>/toggle")
@login_required
def toggle_survey(survey_id: int) -> Response:
    """Toggle survey active status."""
    survey = Survey.query.filter_by(id=survey_id, user_id=current_user.id).first()
    
    if not survey:
        flash("Survey not found")
        return redirect(url_for("surveys.dashboard"))
    
    survey.is_active = not survey.is_active
    db.session.commit()
    
    return redirect(url_for("surveys.dashboard"))


@surveys_bp.route("/s/<int:survey_id>", methods=["GET", "POST"])
def survey_response(survey_id: int) -> str | tuple[str, int]:
    """Public survey response page."""
    survey = Survey.query.filter_by(id=survey_id, is_active=True).first()
    
    if not survey:
        return "Survey not found or inactive", 404
    
    options = SurveyOption.query.filter_by(survey_id=survey_id).order_by(SurveyOption.option_order).all()
    
    if request.method == "POST":
        option_id = request.form.get("option_id")
        respondent_email = request.form.get("email", "").strip()
        
        if not option_id:
            flash("Please select an option")
            return render_template("survey_response.html", survey=survey, options=options)
        
        response = SurveyResponse(
            survey_id=survey_id,
            option_id=int(option_id),
            respondent_email=respondent_email if respondent_email else None
        )
        db.session.add(response)
        db.session.commit()
        
        return render_template("survey_thanks.html")
    
    return render_template("survey_response.html", survey=survey, options=options)


@surveys_bp.route("/survey/<int:survey_id>/results")
@login_required
def survey_results(survey_id: int) -> str | Response:
    """View survey results."""
    survey = Survey.query.filter_by(id=survey_id, user_id=current_user.id).first()
    
    if not survey:
        flash("Survey not found")
        return redirect(url_for("surveys.dashboard"))
    
    results = db.session.query(
        SurveyOption.option_text,
        SurveyOption.option_order,
        func.count(SurveyResponse.id).label("vote_count")
    ).outerjoin(
        SurveyResponse, SurveyOption.id == SurveyResponse.option_id
    ).filter(
        SurveyOption.survey_id == survey_id
    ).group_by(
        SurveyOption.id
    ).order_by(
        SurveyOption.option_order
    ).all()
    
    total_votes = sum(r.vote_count for r in results)
    
    return render_template(
        "survey_results.html",
        survey=survey,
        results=results,
        total_votes=total_votes
    )
