# Intelligent Internship Placement Management System (IIPMS)
# 
IIPMS is a Django and PostgreSQL capstone application for managing internship listings, applications, employer workflows, placement officer monitoring, academic supervisor evaluation, notifications, reporting, and rule-based internship recommendations.

## Features

- Django authentication with role-based dashboards.
- Student portal for profiles, skills, resumes, applications, weekly logs, timesheets, and recommendations.
- Employer portal for company profiles, internship listings, applicant review, interview feedback, and offers.
- Placement officer dashboard for approvals, analytics, CSV export, and PDF export.
- Academic supervisor module for assigned students, weekly log review, and evaluations.
- Weighted matching engine using skills, interests, location, availability, and listing requirements.
- In-app notifications plus Celery task stubs for reminders and expired internship handling.

## Local Setup

1. Create and activate a virtual environment.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies.

```powershell
pip install -r requirements.txt
```

3. Create a PostgreSQL database named `iipms`, then copy `.env.example` values into your environment or set them in PowerShell.

```powershell
$env:POSTGRES_DB="iipms"
$env:POSTGRES_USER="postgres"
$env:POSTGRES_PASSWORD="postgres"
$env:POSTGRES_HOST="localhost"
$env:POSTGRES_PORT="5432"
```


4. Create migrations and migrate.

```powershell
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser and seed demo data.

```powershell
python manage.py createsuperuser
python manage.py seed_demo
```

6. Run the development server.

```powershell
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Demo Accounts

All demo accounts use the password `DemoPass123!`.

- Student: `student`
- Employer: `employer`
- Placement Officer: `officer`
- Academic Supervisor: `supervisor`

## Background Tasks

The project includes Celery tasks in `notifications/tasks.py`:

- `close_expired_internships`
- `send_weekly_log_reminders`
- `send_interview_reminders`

Run a worker when Redis is available:

```powershell
celery -A iipms worker -l info
```


## Security Notes

Django provides password hashing, CSRF protection, template escaping, ORM-based SQL injection protection, and secure session handling. The project adds role decorators, account approval checks, file extension and size validation for resumes, and constrained dashboards per role.
