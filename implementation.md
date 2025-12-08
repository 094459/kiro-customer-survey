# Customer Survey Application - Implementation Specification

## Overview
Build a Customer Survey web application using Flask, SQLite, and Jinja2 templates.

## Technology Stack
- Python 3.12
- Flask (web framework)
- SQLite (database)
- Jinja2 (templates)
- Flask-Login (authentication)
- Werkzeug (password hashing)
- python-dotenv (configuration)

## Authentication

### User Registration
- Users register with email and password
- Passwords are hashed using Werkzeug security
- No email verification required

### User Login
- Email/password authentication
- Session-based authentication using Flask-Login
- Track last_login timestamp

## Features

### Dashboard (Authenticated Users)
- Display application explanation
- List all surveys created by the user
- Show survey status (active/inactive)
- Button to create new survey
- Display shareable link for each survey

### Survey Creation
- Required fields:
  - Title (text, required)
  - Description (text, optional)
- Multiple choice options:
  - Minimum 2 options
  - Maximum 5 options
  - Each option has text and order (1-5)
- New surveys are active by default
- Generate unique shareable link

### Survey Management
- Toggle survey active/inactive status
- Only active surveys accept new responses
- View results for any survey

### Survey Response (Public Access)
- No login required
- Access via shareable link
- Display survey title and description
- Show all available options
- Submit one response per survey
- Optionally collect respondent email
- Prevent duplicate responses (track by session or email)

### Results View (Authenticated Users)
- Display for each option:
  - Option text
  - Vote count
  - Percentage of total votes
- Show total response count
- Only survey creator can view results

## Design Requirements
- Clean, minimal CSS
- Easy to customize styles
- Mobile-responsive layout
- Simple navigation

## Database Schema
Follow the schema defined in `data-model/database_schema.yaml`:
- Users table
- Surveys table
- Survey_Options table
- Survey_Responses table

## Project Structure
```
project/
├── src/
│   ├── __init__.py
│   ├── models.py
│   ├── auth.py
│   ├── surveys.py
│   ├── database.py
│   └── templates/
│       ├── base.html
│       ├── login.html
│       ├── register.html
│       ├── dashboard.html
│       ├── create_survey.html
│       ├── survey_response.html
│       └── survey_results.html
├── static/
│   └── style.css
├── tests/
├── .env.example
└── run.py
```

## Development Guidelines
- Follow Python development standards in `.kiro/steering/python-dev.md`
- Use UV for dependency management
- Use virtual environment
- Store configuration in .env file
- Never commit secrets
- Implement proper error handling
- Use logging module

## Security Requirements
- Hash all passwords
- Sanitize all inputs
- Implement CSRF protection with Flask-WTF
- Prevent SQL injection (use parameterized queries)
- XSS protection (Jinja2 auto-escaping)
- Environment variables for sensitive config

## Implementation Steps
1. Set up project structure and dependencies
2. Initialize database with schema
3. Implement user authentication (register/login)
4. Build dashboard view
5. Implement survey creation
6. Build public survey response page
7. Implement results view
8. Add survey management (activate/deactivate)
9. Apply CSS styling
10. Test all functionality
