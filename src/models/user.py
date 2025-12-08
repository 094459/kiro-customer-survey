# SPDX-License-Identifier: Apache-2.0
# Copyright (2026) Beachgeek.co.uk
# Author: Ricardo Sueiras
# Apache 2.0 license

"""User model."""

from datetime import datetime
from flask_login import UserMixin
from src.extensions import db


class User(UserMixin, db.Model):
    __tablename__ = "users"
    
    id = db.Column("user_id", db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    surveys = db.relationship("Survey", back_populates="user", cascade="all, delete-orphan")
