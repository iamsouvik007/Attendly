# Attendly

Attendly is a Django-based attendance management app for teachers.

It includes:
- Email/password authentication
- Google login (django-allauth)
- Class and student management
- Attendance sessions and attendance marking
- Class and student attendance reports
- Caching for faster repeated reads
- Render deployment support (PostgreSQL + Gunicorn + WhiteNoise)

## Tech Stack

- Python 3.11+
- Django 5.2+
- django-allauth
- PostgreSQL (production via `DATABASE_URL`)
- SQLite (local fallback)
- WhiteNoise (static files in production)
- Gunicorn (production WSGI server)

## Project Structure

Key folders/files:
- `accounts/` auth, registration, login
- `classes/` classes, students, enrollment
- `attendance/` session start and attendance marking
- `reports/` class/student report views
- `dashboard/` teacher dashboard
- `config/` project settings and root urls
- `templates/` all HTML templates (includes landing page)
- `static/` CSS/JS assets
- `render.yaml` Render deployment config
- `.env.example` environment variable template

## Features

- Landing page at `/` for signed-out users
- Dashboard redirect for signed-in users
- Add classes and students
- Student fields:
  - First Name (required)
  - Last Name (required)
  - Roll No (required, unique)
  - Mobile No (required, unique, minimum 10 digits, digits only)
- Attendance record by session
- Report pages with cached read performance

## Local Setup

1. Clone and open the project.
2. Create and activate venv.
3. Install dependencies.
4. Run migrations.
5. Create admin user.
6. Run server.

### Windows PowerShell

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open:
- `http://127.0.0.1:8000/`

## Environment Variables

Copy `.env.example` and set values in your environment.

Required in production:
- `DEBUG=False`
- `SECRET_KEY=<strong-secret>`
- `ALLOWED_HOSTS=<your-domain,localhost,127.0.0.1>`
- `CSRF_TRUSTED_ORIGINS=https://<your-domain>`
- `DATABASE_URL=<render-postgres-external-url>`

Optional:
- `DB_CONN_MAX_AGE=600`
- `CACHE_TIMEOUT=300`
- `GOOGLE_CLIENT_ID=<google-oauth-client-id>`
- `GOOGLE_CLIENT_SECRET=<google-oauth-client-secret>`
- `SECURE_HSTS_SECONDS=31536000`

## Database Configuration

The app uses PostgreSQL only.
`DATABASE_URL` is required in all environments.

Quick check command:

```powershell
python -c "import os,django; os.environ.setdefault('DJANGO_SETTINGS_MODULE','config.settings'); django.setup(); from django.conf import settings; print(settings.DATABASES['default']['ENGINE'])"
```

Expected output:
- `django.db.backends.postgresql`

## Google Login Setup

1. In Google Cloud Console, create OAuth credentials.
2. Add authorized redirect URI:
   - `http://localhost:8000/accounts/google/login/callback/` (local)
   - `https://<your-render-domain>/accounts/google/login/callback/` (production)
3. Set environment vars:
   - `GOOGLE_CLIENT_ID`
   - `GOOGLE_CLIENT_SECRET`
4. In Django admin:
   - Ensure `Site` domain matches your environment
   - Ensure Google SocialApp exists and is linked to that Site

## Caching

- Configured via Django cache framework in settings.
- Default cache backend: `LocMemCache`.
- Cached areas include dashboard and report reads.
- Relevant write actions invalidate related cache keys.

## Render Deployment

This repository includes:
- `render.yaml`
- `Procfile`
- `runtime.txt`

Render build command:
- Install dependencies
- Collect static files
- Run migrations

Render start command:
- `gunicorn config.wsgi:application --log-file -`

### Deploy Steps

1. Push repo to GitHub.
2. Create a new Web Service on Render.
3. Connect repo and use existing `render.yaml`.
4. Create/attach PostgreSQL on Render.
5. Set `DATABASE_URL` in Render environment.
6. Confirm `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` match your Render domain.
7. Deploy.

## Security Notes

Production security settings are enabled when `DEBUG=False`:
- SSL redirect
- Secure cookies
- HSTS
- X-Frame-Options DENY
- Content type sniff protection

Do not commit real secrets or database URLs to source control.

## Useful Commands

```powershell
python manage.py check
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
```

## Troubleshooting

### 1) Google login `redirect_uri_mismatch`
- Ensure callback URI in Google Cloud exactly matches app callback.

### 2) Login error about missing username field
- Confirm custom user model is configured with email login and allauth settings.

### 3) App still using SQLite in production
- Check `DATABASE_URL` is set in environment.

### 4) Static files not loading on Render
- Ensure `collectstatic` runs during build and WhiteNoise dependency is installed.

## License

Internal project / personal use unless you add your own license.
