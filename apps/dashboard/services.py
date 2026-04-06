from django.utils import timezone

from apps.accounts.models import User
from apps.assessments.models import Assessment
from apps.assessments.serializers import AssessmentSerializer
from apps.auditlog.models import AuditLog
from apps.notifications.models import Notification
from apps.notifications.serializers import NotificationSerializer
from apps.planner.models import PlannerLog, StudyPlan
from apps.planner.serializers import StudySessionSerializer
from apps.progress.services import ProgressService
from apps.scheduler.models import ScheduledJob


class DashboardService:
    @staticmethod
    def student_dashboard(user):
        ProgressService.sync_all_subject_progress(user)
        today = timezone.localdate()
        today_sessions = user.study_sessions.filter(session_date=today).order_by("start_time")[:5]
        upcoming_deadlines = user.assessments.filter(status__in=["pending", "in_progress", "overdue"]).order_by("due_date")[:5]
        overdue_count = user.assessments.filter(status="overdue").count()
        stats = ProgressService.overview(user)
        notification_preview = Notification.objects.filter(user=user).order_by("-created_at")[:5]
        quick_chart = ProgressService.weekly_metrics(user)
        return {
            "welcomeInfo": {"name": user.full_name, "role": user.role},
            "todaySessions": StudySessionSerializer(today_sessions, many=True).data,
            "upcomingDeadlines": AssessmentSerializer(upcoming_deadlines, many=True).data,
            "overdueCount": overdue_count,
            "statsCards": stats,
            "notificationPreview": NotificationSerializer(notification_preview, many=True).data,
            "quickChartData": quick_chart,
        }

    @staticmethod
    def admin_dashboard():
        return {
            "totalUsers": User.objects.count(),
            "activeStudents": User.objects.filter(role="student", is_active=True).count(),
            "assessmentsCount": Assessment.objects.count(),
            "generatedPlansCount": StudyPlan.objects.count(),
            "notificationsCount": Notification.objects.count(),
            "schedulerJobStats": {
                "queued": ScheduledJob.objects.filter(status="queued").count(),
                "running": ScheduledJob.objects.filter(status="running").count(),
                "completed": ScheduledJob.objects.filter(status="completed").count(),
                "failed": ScheduledJob.objects.filter(status="failed").count(),
            },
            "recentLogs": {
                "planner": list(PlannerLog.objects.values("id", "status", "message")[:5]),
                "audit": list(AuditLog.objects.values("id", "action", "target_model", "created_at")[:5]),
            },
        }
