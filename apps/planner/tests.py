import pytest
from rest_framework.test import APIClient

from apps.accounts.models import StudentProfile, User
from apps.assessments.models import Assessment
from apps.subjects.models import Subject


@pytest.mark.django_db
def test_generate_plan_creates_sessions():
    user = User.objects.create_user(email="planner@example.com", password="demo123", full_name="Planner User")
    StudentProfile.objects.create(user=user)
    subject = Subject.objects.create(user=user, name="Algorithms", code="CS201")
    Assessment.objects.create(
        user=user,
        subject=subject,
        title="Exam Prep",
        assessment_type="exam",
        due_date="2026-04-20",
        weight_percentage=30,
        estimated_hours=4,
        status="pending",
    )

    client = APIClient()
    login = client.post("/api/auth/login/", {"email": "planner@example.com", "password": "demo123"}, format="json")
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {login.data['data']['access']}")
    response = client.post("/api/planner/generate/", {}, format="json")

    assert response.status_code == 201
    assert response.data["data"]["sessions"]

# Create your tests here.
