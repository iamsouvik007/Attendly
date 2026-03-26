# Attendly 👋

Attendly is a Django-based attendance management platform for teachers. It helps manage classes and students, run attendance sessions, and view attendance reports from a clean dashboard.

## Live Demo 🔗

https://attendly-77r3.onrender.com

## Features

- Email/password authentication
- Google sign-in using django-allauth
- Teacher profile flow
- Class creation and management
- Student management with validation for unique roll number and phone
- Attendance session start and attendance marking
- Class-wise and student-wise attendance reports
- Cached reads for dashboard and report pages
- Production-ready deployment setup for Render

## Tech Stack

- Python 3.11+
- Django 6.0.3
- PostgreSQL (required via DATABASE_URL)
- django-allauth
- Gunicorn
- WhiteNoise

## Project Structure

- accounts/: authentication, registration, profile, social login integration
- classes/: class and student models, forms, views
- attendance/: attendance session flow and marking views
- reports/: report views for class and student attendance
- dashboard/: home dashboard
- config/: project settings and root URL config
- templates/: HTML templates for all apps
- static/: custom CSS and JavaScript
- render.yaml / Procfile / runtime.txt: Render deployment configuration

## Quick Start (Local)

1. Clone the repository and open it.
2. Create and activate a virtual environment.
3. Install dependencies.
4. Set required environment variables.
5. Run migrations and start the server.

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Create a .env file in the project root:

```env
DEBUG=True
SECRET_KEY=change-this-in-production
ALLOWED_HOSTS=127.0.0.1,localhost
CSRF_TRUSTED_ORIGINS=
DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/DBNAME
```

Run the app:

```powershell
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open: http://127.0.0.1:8000/

## Environment Variables

Required:

- SECRET_KEY
- DATABASE_URL

Recommended:

- DEBUG (True/False)
- ALLOWED_HOSTS (comma-separated)
- CSRF_TRUSTED_ORIGINS (comma-separated full origins)
- DB_CONN_MAX_AGE (default: 600)
- CACHE_TIMEOUT (default: 300)
- GOOGLE_CLIENT_ID
- GOOGLE_CLIENT_SECRET
- SECURE_HSTS_SECONDS (default: 31536000)

## Google Login Setup

1. Create OAuth credentials in Google Cloud Console.
2. Add redirect URIs:
   - http://localhost:8000/accounts/google/login/callback/
   - https://attendly-77r3.onrender.com/accounts/google/login/callback/
3. Set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET.
4. In Django admin, verify:
   - Site domain is correct for your environment.
   - A Google SocialApp is linked to that Site.

## Deployment (Render)

This project includes production deployment files:

- render.yaml
- Procfile
- runtime.txt

Standard flow:

1. Push this repository to GitHub.
2. Create a Render Web Service from the repo.
3. Attach a PostgreSQL database.
4. Set environment variables on Render.
5. Deploy and run migrations.

Start command:

```bash
gunicorn config.wsgi:application --log-file -
```

## Useful Commands

```powershell
python manage.py check
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
```

## Security Notes

When DEBUG=False, the app enables security-focused settings such as HTTPS redirect, secure cookies, HSTS, and protective headers. Never commit real secrets to source control.

## create with ❤️ by vik
