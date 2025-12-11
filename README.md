# Customer Survey Application

A Flask-based web application for creating and managing customer surveys.

## Features

- User registration and authentication
- Create surveys with 2-5 multiple choice options
- Share surveys via public links
- Collect responses without requiring login
- View results with vote counts and percentages
- Toggle surveys active/inactive
- Mobile-responsive design

## Setup

1. Install dependencies:
```bash
uv venv
source .venv/bin/activate
uv pip install -e .
```

2. Configure environment:
```bash
cp .env.example .env
# Edit .env and set SECRET_KEY for production
```

3. Run the application:

**Development:**
```bash
python run.py
```

**Production with Gunicorn:**
```bash
uv run gunicorn -c gunicorn.conf.py run:app
```

The app will be available at http://localhost:5000 (development) or http://localhost:8000 (production)

## Usage

1. Register a new account at `/register`
2. Login at `/login`
3. Create surveys from the dashboard
4. Share survey links with respondents
5. View results from the dashboard

## Project Structure

```
project/
├── src/
│   ├── __init__.py          # Flask app factory
│   ├── extensions.py        # Flask extensions
│   ├── models/              # SQLAlchemy models
│   │   ├── user.py
│   │   └── survey.py
│   ├── routes/              # Route blueprints
│   │   ├── auth.py
│   │   └── surveys.py
│   ├── static/              # CSS and assets
│   └── templates/           # Jinja2 templates
├── tests/                   # Unit tests
├── .env                     # Configuration
└── run.py                   # Entry point
```

## Testing

Run tests with coverage:
```bash
./run_tests.sh
```

Or manually:
```bash
PYTHONPATH=$(pwd) uv run pytest
```

Current test coverage: **99%** (34 tests)

## Security

- Passwords are hashed using Werkzeug
- CSRF protection enabled
- SQL injection prevention via parameterized queries
- XSS protection via Jinja2 auto-escaping
- Environment variables for sensitive config
