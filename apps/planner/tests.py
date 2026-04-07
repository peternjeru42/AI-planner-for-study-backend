import pytest
from rest_framework.test import APIClient

from apps.accounts.models import StudentProfile, User
from apps.assessments.models import Assessment
from apps.planner.ai_service import PlannerAIService
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


@pytest.mark.django_db
def test_ai_models_endpoint_returns_supported_models():
    user = User.objects.create_user(email="ai-models@example.com", password="demo123", full_name="AI Models User")
    StudentProfile.objects.create(user=user)

    client = APIClient()
    login = client.post("/api/auth/login/", {"email": "ai-models@example.com", "password": "demo123"}, format="json")
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {login.data['data']['access']}")
    response = client.get("/api/planner/ai/models/")

    assert response.status_code == 200
    assert response.data["data"]
    assert any(item["recommended"] for item in response.data["data"])


@pytest.mark.django_db
def test_ai_assistant_endpoint_returns_guidance(monkeypatch, settings):
    user = User.objects.create_user(email="ai-assistant@example.com", password="demo123", full_name="AI Assistant User")
    StudentProfile.objects.create(user=user, course_name="Computer Science")
    subject = Subject.objects.create(user=user, name="Algorithms", code="CS201")
    Assessment.objects.create(
        user=user,
        subject=subject,
        title="Final Exam",
        assessment_type="exam",
        due_date="2026-04-20",
        weight_percentage=40,
        estimated_hours=5,
        status="pending",
    )
    settings.OPENAI_API_KEY = "test-key"

    def fake_request_completion(*, api_key, model, messages):
        assert api_key == "test-key"
        assert model == "gpt-5-mini"
        assert messages
        return {"choices": [{"message": {"content": "Prioritize Algorithms first and protect two focused sessions this week."}}]}

    monkeypatch.setattr(PlannerAIService, "_request_completion", fake_request_completion)

    client = APIClient()
    login = client.post("/api/auth/login/", {"email": "ai-assistant@example.com", "password": "demo123"}, format="json")
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {login.data['data']['access']}")
    response = client.post(
        "/api/planner/ai/assistant/",
        {"model": "gpt-5-mini", "question": "How should I prioritize this week?"},
        format="json",
    )

    assert response.status_code == 200
    assert response.data["data"]["model"] == "gpt-5-mini"
    assert "Prioritize Algorithms" in response.data["data"]["answer"]

# Create your tests here.
