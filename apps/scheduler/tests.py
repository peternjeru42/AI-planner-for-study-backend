import pytest
from rest_framework.test import APIClient

from apps.accounts.models import User


@pytest.mark.django_db
def test_admin_can_simulate_scheduler_cycle():
    admin = User.objects.create_user(
        email="admin@example.com",
        password="demo123",
        full_name="Admin",
        role="admin",
        is_staff=True,
        is_superuser=True,
    )

    client = APIClient()
    login = client.post("/api/auth/login/", {"email": "admin@example.com", "password": "demo123"}, format="json")
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {login.data['data']['access']}")
    response = client.post("/api/scheduler/simulate-cycle/", {}, format="json")

    assert response.status_code == 201
    assert response.data["success"] is True

# Create your tests here.
