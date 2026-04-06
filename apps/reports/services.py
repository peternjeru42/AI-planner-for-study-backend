import csv
import io
from datetime import timedelta

from django.db.models import Sum
from django.utils import timezone

from apps.assessments.services import AssessmentService
from apps.planner.models import StudySession
from apps.progress.models import SubjectProgress
from apps.reports.models import WeeklyMetricsSnapshot


class ReportService:
    @staticmethod
    def weekly(user):
        week_start = timezone.localdate() - timedelta(days=6)
        sessions = StudySession.objects.filter(user=user, session_date__gte=week_start)
        planned = sessions.aggregate(total=Sum("duration_minutes"))["total"] or 0
        completed = sessions.filter(status="completed").aggregate(total=Sum("duration_minutes"))["total"] or 0
        tasks_completed = user.assessments.filter(status="completed", updated_at__date__gte=week_start).count()
        overdue_count = user.assessments.filter(status="overdue").count()
        completion_rate = round((completed / planned) * 100, 2) if planned else 0
        snapshot, _ = WeeklyMetricsSnapshot.objects.update_or_create(
            user=user,
            week_start=week_start,
            defaults={
                "tasks_completed": tasks_completed,
                "study_minutes_completed": completed,
                "study_minutes_planned": planned,
                "completion_rate": completion_rate,
                "overdue_count": overdue_count,
            },
        )
        return snapshot

    @staticmethod
    def monthly(user):
        start = timezone.localdate() - timedelta(days=29)
        sessions = StudySession.objects.filter(user=user, session_date__gte=start)
        return {
            "studyMinutes": sessions.aggregate(total=Sum("duration_minutes"))["total"] or 0,
            "completedSessions": sessions.filter(status="completed").count(),
            "plannedSessions": sessions.count(),
            "completedAssessments": user.assessments.filter(status="completed", updated_at__date__gte=start).count(),
        }

    @staticmethod
    def completion_trend(user):
        rows = []
        for week_offset in range(4):
            start = timezone.localdate() - timedelta(days=(week_offset * 7) + 6)
            end = start + timedelta(days=6)
            sessions = StudySession.objects.filter(user=user, session_date__range=(start, end))
            planned = sessions.aggregate(total=Sum("duration_minutes"))["total"] or 0
            completed = sessions.filter(status="completed").aggregate(total=Sum("duration_minutes"))["total"] or 0
            rows.append(
                {
                    "label": f"Week {4 - week_offset}",
                    "completionRate": round((completed / planned) * 100, 2) if planned else 0,
                }
            )
        rows.reverse()
        return rows

    @staticmethod
    def study_hours_by_subject(user):
        queryset = SubjectProgress.objects.filter(user=user).select_related("subject").order_by("subject__code")
        return [{"subject": item.subject.code, "hours": round(item.total_completed_minutes / 60, 2)} for item in queryset]

    @staticmethod
    def deadlines_by_subject(user):
        return [{"subject": item["subject__code"], "count": item["count"]} for item in AssessmentService.deadlines_by_subject(user)]

    @staticmethod
    def export_csv(user):
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Subject", "Completion Rate", "Study Hours"])
        for item in SubjectProgress.objects.filter(user=user).select_related("subject"):
            writer.writerow([item.subject.code, item.completion_rate, round(item.total_completed_minutes / 60, 2)])
        return output.getvalue()
