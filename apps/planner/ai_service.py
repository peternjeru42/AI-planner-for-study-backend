import json
from datetime import timedelta
from urllib import error, request

from django.conf import settings
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.assessments.models import Assessment
from apps.planner.models import StudySession
from apps.subjects.models import Subject


class PlannerAIService:
    MODEL_OPTIONS = [
        {
            "id": "gpt-5-mini",
            "label": "GPT-5 mini",
            "description": "Recommended balance of quality, speed, and cost for study coaching.",
            "recommended": True,
        },
        {
            "id": "gpt-5",
            "label": "GPT-5",
            "description": "Highest-quality reasoning for more detailed planning advice.",
            "recommended": False,
        },
        {
            "id": "gpt-5-nano",
            "label": "GPT-5 nano",
            "description": "Fastest and cheapest option for short planning prompts.",
            "recommended": False,
        },
    ]
    MODEL_IDS = {item["id"] for item in MODEL_OPTIONS}
    API_URL = "https://api.openai.com/v1/chat/completions"

    @classmethod
    def supported_models(cls):
        return cls.MODEL_OPTIONS

    @staticmethod
    def _extract_text(payload):
        choices = payload.get("choices") or []
        if not choices:
            raise ValidationError("OpenAI returned no choices.")

        message = choices[0].get("message") or {}
        content = message.get("content", "")
        if isinstance(content, str):
            return content.strip()

        if isinstance(content, list):
            fragments = []
            for item in content:
                if isinstance(item, dict) and item.get("type") == "text" and item.get("text"):
                    fragments.append(item["text"])
            if fragments:
                return "\n".join(fragments).strip()

        raise ValidationError("OpenAI returned an unexpected response format.")

    @classmethod
    def _build_context(cls, user):
        profile = user.student_profile
        today = timezone.localdate()
        subjects = list(Subject.objects.filter(user=user, is_active=True).order_by("name")[:8])
        assessments = list(
            Assessment.objects.filter(user=user, status__in=["pending", "in_progress", "overdue"])
            .select_related("subject")
            .order_by("due_date", "due_time")[:10]
        )
        sessions = list(
            StudySession.objects.filter(user=user, session_date__range=(today, today + timedelta(days=7)))
            .select_related("subject", "assessment")
            .order_by("session_date", "start_time")[:12]
        )

        return {
            "student": {
                "name": user.full_name,
                "courseName": profile.course_name,
                "yearOfStudy": profile.year_of_study,
                "institutionName": profile.institution_name,
                "timezone": profile.timezone,
                "preferences": {
                    "studyStart": profile.preferred_study_start_time.strftime("%H:%M"),
                    "studyEnd": profile.preferred_study_end_time.strftime("%H:%M"),
                    "sessionLengthMinutes": profile.preferred_session_length_minutes,
                    "breakLengthMinutes": profile.preferred_break_length_minutes,
                    "maxSessionsPerDay": profile.max_sessions_per_day,
                    "weekendAvailable": profile.weekend_available,
                },
            },
            "subjects": [{"name": item.name, "code": item.code, "semester": item.semester or ""} for item in subjects],
            "assessments": [
                {
                    "title": item.title,
                    "subject": item.subject.name,
                    "type": item.assessment_type,
                    "status": item.status,
                    "dueDate": item.due_date.isoformat(),
                    "dueTime": item.due_time.strftime("%H:%M") if item.due_time else None,
                    "estimatedHours": float(item.estimated_hours),
                    "weightPercentage": float(item.weight_percentage),
                }
                for item in assessments
            ],
            "sessions": [
                {
                    "title": item.title,
                    "subject": item.subject.name if item.subject else None,
                    "sessionDate": item.session_date.isoformat(),
                    "startTime": item.start_time.strftime("%H:%M"),
                    "endTime": item.end_time.strftime("%H:%M"),
                    "durationMinutes": item.duration_minutes,
                    "status": item.status,
                }
                for item in sessions
            ],
        }

    @classmethod
    def _request_completion(cls, *, api_key, model, messages):
        payload = json.dumps(
            {
                "model": model,
                "messages": messages,
            }
        ).encode("utf-8")
        req = request.Request(
            cls.API_URL,
            data=payload,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with request.urlopen(req, timeout=60) as response:
                return json.loads(response.read().decode("utf-8"))
        except error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="ignore")
            try:
                message = json.loads(detail).get("error", {}).get("message") or "OpenAI request failed."
            except json.JSONDecodeError:
                message = "OpenAI request failed."
            raise ValidationError(message) from exc
        except error.URLError as exc:
            raise ValidationError("Unable to reach OpenAI from the backend service.") from exc

    @classmethod
    def study_assistant(cls, *, user, question, model=None):
        if model and model not in cls.MODEL_IDS:
            raise ValidationError({"model": "Unsupported model selected."})

        api_key = getattr(settings, "OPENAI_API_KEY", None)
        if not api_key:
            raise ValidationError("OPENAI_API_KEY is not configured.")

        selected_model = model or getattr(settings, "OPENAI_DEFAULT_MODEL", "gpt-5-mini")
        if selected_model not in cls.MODEL_IDS:
            selected_model = "gpt-5-mini"

        context = cls._build_context(user)
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an academic study coach inside StudyFlow. "
                    "Use only the provided student context. "
                    "Be practical, structured, and concise. "
                    "Give advice tailored to workload, deadlines, and study preferences. "
                    "Prefer short sections with flat bullet points."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Student context:\n{json.dumps(context, indent=2)}\n\n"
                    f"Question: {question}\n\n"
                    "Respond with:\n"
                    "1. A short direct answer.\n"
                    "2. A prioritized action plan.\n"
                    "3. Any schedule risks you notice.\n"
                ),
            },
        ]

        payload = cls._request_completion(api_key=api_key, model=selected_model, messages=messages)
        return {
            "model": selected_model,
            "question": question,
            "answer": cls._extract_text(payload),
            "contextSummary": {
                "subjectsCount": len(context["subjects"]),
                "assessmentsCount": len(context["assessments"]),
                "sessionsCount": len(context["sessions"]),
            },
        }
