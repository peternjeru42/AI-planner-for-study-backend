import pytest
from rest_framework.test import APIClient

from apps.accounts.models import StudentProfile, User
from apps.subjects.models import Subject


@pytest.mark.django_db
def test_student_sees_only_own_subjects():
    owner = User.objects.create_user(email="owner@example.com", password="demo123", full_name="Owner")
    other = User.objects.create_user(email="other@example.com", password="demo123", full_name="Other")
    StudentProfile.objects.create(user=owner)
    StudentProfile.objects.create(user=other)
    Subject.objects.create(user=owner, name="Algorithms", code="CS201")
    Subject.objects.create(user=other, name="Physics", code="PHY101")

    client = APIClient()
    login = client.post("/api/auth/login/", {"email": "owner@example.com", "password": "demo123"}, format="json")
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {login.data['data']['access']}")
    response = client.get("/api/subjects/")

    assert response.status_code == 200
    assert len(response.data["data"]) == 1
    assert response.data["data"][0]["code"] == "CS201"

# Create your tests here.
