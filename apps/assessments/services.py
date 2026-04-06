from datetime import date

from django.db.models import Count

from apps.assessments.models import Assessment


class AssessmentService:
    STATUS_PRIORITY = {
        "pending": 1.0,
        "in_progress": 0.6,
        "completed": 0.0,
        "missed": 0.2,
        "overdue": 1.0,
    }

    @classmethod
    def calculate_priority_score(cls, assessment: Assessment) -> float:
        days_until_deadline = max((assessment.due_date - date.today()).days, 0)
        deadline_urgency = max(0, 100 - min(days_until_deadline, 100))
        weight_component = assessment.weight_percentage
        effort_component = float(assessment.estimated_hours)
        status_gap = cls.STATUS_PRIORITY.get(assessment.status, 0)
        overdue_bonus = 20 if assessment.due_date < date.today() else 0
        exam_bonus = 15 if assessment.assessment_type == "exam" else 0
        manual_bonus = {"high": 12, "medium": 6, "low": 0}.get(assessment.manual_priority or "", 0)
        return round(
            (deadline_urgency * 0.40)
            + (weight_component * 0.25)
            + (effort_component * 0.20)
            + (status_gap * 100 * 0.15)
            + overdue_bonus
            + exam_bonus
            + manual_bonus,
            2,
        )

    @classmethod
    def refresh_assessment(cls, assessment: Assessment) -> Assessment:
        if assessment.status not in {"completed", "missed"} and assessment.due_date < date.today():
            assessment.status = "overdue"
        assessment.calculated_priority_score = cls.calculate_priority_score(assessment)
        assessment.save(update_fields=["status", "calculated_priority_score", "updated_at"])
        return assessment

    @classmethod
    def update_overdue_items(cls, queryset):
        for assessment in queryset:
            cls.refresh_assessment(assessment)

    @staticmethod
    def filter_options():
        return {
            "types": [choice[0] for choice in Assessment._meta.get_field("assessment_type").choices],
            "statuses": ["pending", "in-progress", "completed", "missed", "overdue"],
        }

    @staticmethod
    def deadlines_by_subject(user):
        return (
            Assessment.objects.filter(user=user)
            .values("subject__code")
            .annotate(count=Count("id"))
            .order_by("subject__code")
        )
