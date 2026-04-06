# AI Study Planner Backend

Django REST backend for StudyFlow.

## Stack

- Django
- Django REST Framework
- PostgreSQL-ready settings
- JWT authentication
- Django Admin

## Run locally

```bash
python -m venv .venv
. .venv/Scripts/activate
pip install -r requirements/dev.txt
python manage.py migrate
python manage.py seed_demo_data
python manage.py runserver
```

## API

- Base URL: `/api/`
- Health check: `/api/health/`
- Admin: `/admin/`

## Notes

- Email and scheduler flows are simulated through database-backed endpoints and logs.
- Demo seed command creates student and admin accounts for frontend integration.
