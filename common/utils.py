from datetime import datetime, time

from rest_framework.response import Response


def api_success(data=None, message="Request completed successfully.", status_code=200):
    return Response({"success": True, "message": message, "data": data}, status=status_code)


def api_error(message="Request failed.", errors=None, status_code=400):
    payload = {"success": False, "message": message}
    if errors is not None:
        payload["errors"] = errors
    return Response(payload, status=status_code)


def snake_to_frontend(value: str) -> str:
    mapping = {
        "in_progress": "in-progress",
        "deadline_reminder": "deadline-reminder",
        "study_session_reminder": "session-reminder",
        "overdue_alert": "overdue-alert",
        "plan_generated": "daily-plan",
        "weekly_report": "weekly-summary",
        "in_app": "in-app",
    }
    return mapping.get(value, value)


def parse_time_string(value: str) -> time:
    return datetime.strptime(value, "%H:%M").time()
