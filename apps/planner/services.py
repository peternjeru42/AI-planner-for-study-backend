from datetime import date, datetime, timedelta

from django.db import transaction
from django.utils import timezone

from apps.assessments.models import Assessment
from apps.assessments.services import AssessmentService
from apps.notifications.services import NotificationService
from apps.planner.models import PlannerLog, StudyPlan, StudySession
from apps.progress.services import ProgressService


class PlannerService:
    SESSION_TYPE_MAP = {
        "assignment": "assignment_work",
        "cat": "revision",
        "quiz": "revision",
        "exam": "exam_prep",
        "project": "project_work",
        "presentation": "project_work",
    }

    @staticmethod
    def _time_add(base_time, minutes):
        dt = datetime.combine(date.today(), base_time) + timedelta(minutes=minutes)
        return dt.time()

    @classmethod
    def _build_sessions(cls, *, user, plan, assessments, start_date, end_date):
        profile = user.student_profile
        sessions = []
        current_date = max(start_date, timezone.localdate())
        current_time = profile.preferred_study_start_time
        sessions_per_day = 0

        for assessment in assessments:
            if current_date > end_date:
                break
            sessions_needed = max(1, int(round((float(assessment.estimated_hours) * 60) / profile.preferred_session_length_minutes + 0.49)))
            for index in range(sessions_needed):
                while True:
                    if current_date > end_date:
                        break
                    if not profile.weekend_available and current_date.weekday() >= 5:
                        current_date += timedelta(days=1)
                        current_time = profile.preferred_study_start_time
                        sessions_per_day = 0
                        continue
                    if sessions_per_day >= profile.max_sessions_per_day:
                        current_date += timedelta(days=1)
                        current_time = profile.preferred_study_start_time
                        sessions_per_day = 0
                        continue
                    end_time = cls._time_add(current_time, profile.preferred_session_length_minutes)
                    if end_time > profile.preferred_study_end_time:
                        current_date += timedelta(days=1)
                        current_time = profile.preferred_study_start_time
                        sessions_per_day = 0
                        continue
                    break

                if current_date > end_date:
                    break

                session = StudySession.objects.create(
                    study_plan=plan,
                    user=user,
                    subject=assessment.subject,
                    assessment=assessment,
                    title=f"{assessment.title} - Session {index + 1}",
                    session_date=current_date,
                    start_time=current_time,
                    end_time=end_time,
                    duration_minutes=profile.preferred_session_length_minutes,
                    session_type=cls.SESSION_TYPE_MAP.get(assessment.assessment_type, "revision"),
                    priority_score=assessment.calculated_priority_score,
                    status="planned",
                )
                sessions.append(session)
                sessions_per_day += 1
                current_time = cls._time_add(end_time, profile.preferred_break_length_minutes)
        return sessions

    @classmethod
    @transaction.atomic
    def generate_plan(cls, *, user, startDate=None, endDate=None, title="", trigger="manual", regenerate=False):
        start_date = startDate or timezone.localdate()
        end_date = endDate or (start_date + timedelta(days=13))

        active_plan = StudyPlan.objects.filter(user=user, status="active").first()
        if regenerate and active_plan:
            active_plan.status = "archived"
            active_plan.save(update_fields=["status", "updated_at"])
            active_plan.sessions.filter(status="planned", session_date__gte=timezone.localdate()).update(status="rescheduled")

        assessments = list(
            Assessment.objects.filter(user=user, status__in=["pending", "in_progress", "overdue"])
            .select_related("subject")
            .order_by("due_date", "due_time")
        )
        for assessment in assessments:
            AssessmentService.refresh_assessment(assessment)
        assessments.sort(key=lambda item: item.calculated_priority_score, reverse=True)

        plan = StudyPlan.objects.create(
            user=user,
            title=title or f"Study Plan {start_date.isoformat()} to {end_date.isoformat()}",
            generated_for_start_date=start_date,
            generated_for_end_date=end_date,
            generation_trigger=trigger,
            status="active",
        )

        sessions = cls._build_sessions(
            user=user,
            plan=plan,
            assessments=assessments,
            start_date=start_date,
            end_date=end_date,
        )
        PlannerLog.objects.create(
            user=user,
            study_plan=plan,
            trigger_source=trigger,
            input_snapshot_json={
                "assessmentIds": [str(item.id) for item in assessments],
                "startDate": start_date.isoformat(),
                "endDate": end_date.isoformat(),
            },
            output_snapshot_json={"sessionIds": [str(item.id) for item in sessions], "sessionsCreated": len(sessions)},
            status="completed",
            message=f"Generated {len(sessions)} sessions.",
        )
        ProgressService.sync_all_subject_progress(user)
        NotificationService.plan_generated(user, plan)
        return plan, sessions

    @staticmethod
    def current_plan(user):
        return StudyPlan.objects.filter(user=user, status="active").prefetch_related("sessions").first()

    @staticmethod
    def reschedule_session(*, session, sessionDate, startTime, endTime=None):
        session.session_date = sessionDate
        session.start_time = startTime
        session.end_time = endTime or PlannerService._time_add(startTime, session.duration_minutes)
        session.status = "rescheduled"
        session.save(update_fields=["session_date", "start_time", "end_time", "status", "updated_at"])
        return session
