import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_register_returns_tokens_and_profile():
    client = APIClient()
    response = client.post(
        "/api/auth/register/",
        {
            "fullName": "Test Student",
            "email": "test-student@example.com",
            "password": "strongpass123",
            "passwordConfirm": "strongpass123",
        },
        format="json",
    )

    assert response.status_code == 201
    assert response.data["success"] is True
    assert response.data["data"]["user"]["email"] == "test-student@example.com"
    assert "access" in response.data["data"]

# Create your tests here.
