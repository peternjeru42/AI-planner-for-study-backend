from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from apps.accounts.models import User
from apps.assessments.services import AssessmentService
from apps.notifications.services import NotificationService
from apps.planner.services import PlannerService
from apps.reports.services import ReportService
from apps.scheduler.models import JobRunHistory, ScheduledJob


class SchedulerService:
    DEFAULT_JOBS = [
        ("morning_plan_generation", "planner"),
        ("deadline_check", "notifications"),
        ("overdue_scan", "assessments"),
        ("weekly_summary", "reports"),
    ]

    @staticmethod
    def create_job(*, name, job_type, target_user=None, payload=None):
        return ScheduledJob.objects.create(
            name=name,
            job_type=job_type,
            status="queued",
            scheduled_time=timezone.now() + timedelta(hours=24),
            target_user=target_user,
            payload_json=payload or {},
        )

    @classmethod
    @transaction.atomic
    def run_job(cls, job: ScheduledJob):
        start_time = timezone.now()
        job.status = "running"
        job.started_at = start_time
        job.save(update_fields=["status", "started_at"])
        output = ""
        target_users = [job.target_user] if job.target_user else list(User.objects.filter(role="student"))
        try:
            if job.name == "morning_plan_generation":
                for user in target_users:
                    plan, sessions = PlannerService.generate_plan(user=user, trigger="scheduler")
                    output += f"Generated {len(sessions)} sessions for {user.email}. "
            elif job.name == "deadline_check":
                for user in target_users:
                    notifications = NotificationService.trigger_due_notifications(user)
                    output += f"Triggered {len(notifications)} notifications for {user.email}. "
            elif job.name == "overdue_scan":
                for user in target_users:
                    queryset = user.assessments.all()
                    AssessmentService.update_overdue_items(queryset)
                    output += f"Overdue scan completed for {user.email}. "
            elif job.name == "weekly_summary":
                for user in target_users:
                    snapshot = ReportService.weekly(user)
                    NotificationService.create_notification(
                        user=user,
                        title="Weekly summary",
                        message="Your weekly study summary is ready.",
                        notification_type="weekly_report",
                        channel="email",
                        status="queued",
                        is_simulated=True,
                    )
                    output += f"Weekly snapshot created for {user.email} ({snapshot.tasks_completed} tasks). "
                NotificationService.simulate_email_dispatch()
            else:
                output = "No-op job run."
            job.status = "completed"
        except Exception as exc:  # noqa: BLE001
            output = str(exc)
            job.status = "failed"
        job.ended_at = timezone.now()
        job.result_message = output
        job.save(update_fields=["status", "ended_at", "result_message"])
        history = JobRunHistory.objects.create(
            scheduled_job=job,
            run_status=job.status,
            run_started_at=start_time,
            run_ended_at=job.ended_at,
            output_log=output,
        )
        return job, history

    @classmethod
    def simulate_cycle(cls):
        results = []
        for name, job_type in cls.DEFAULT_JOBS:
            job = cls.create_job(name=name, job_type=job_type)
            results.append(cls.run_job(job)[0])
        return results
