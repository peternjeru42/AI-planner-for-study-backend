from datetime import datetime, timedelta

from django.db.models import Count, Sum
from django.utils import timezone

from apps.assessments.models import Assessment
from apps.planner.models import StudySession
from apps.progress.models import AssessmentProgress, StudySessionCompletion, SubjectProgress


class ProgressService:
    @staticmethod
    def sync_subject_progress_for_subject(subject):
        assessments = subject.assessments.all()
        sessions = subject.study_sessions.all()
        total_assessments = assessments.count()
        completed_assessments = assessments.filter(status="completed").count()
        total_planned_minutes = sessions.aggregate(total=Sum("duration_minutes"))["total"] or 0
        total_completed_minutes = sessions.filter(status="completed").aggregate(total=Sum("duration_minutes"))["total"] or 0
        completion_rate = round((completed_assessments / total_assessments) * 100, 2) if total_assessments else 0
        progress, _ = SubjectProgress.objects.update_or_create(
            subject=subject,
            user=subject.user,
            defaults={
                "total_assessments": total_assessments,
                "completed_assessments": completed_assessments,
                "total_planned_minutes": total_planned_minutes,
                "total_completed_minutes": total_completed_minutes,
                "completion_rate": completion_rate,
            },
        )
        return progress

    @classmethod
    def sync_all_subject_progress(cls, user):
        return [cls.sync_subject_progress_for_subject(subject) for subject in user.subjects.all()]

    @staticmethod
    def mark_session_complete(session: StudySession, *, actual_minutes=None, remarks=""):
        session.status = "completed"
        session.save(update_fields=["status", "updated_at"])
        completion, _ = StudySessionCompletion.objects.update_or_create(
            study_session=session,
            user=session.user,
            defaults={
                "completed_at": timezone.now(),
                "actual_minutes": actual_minutes or session.duration_minutes,
                "completion_status": "completed",
                "remarks": remarks,
            },
        )
        ProgressService.sync_subject_progress_for_subject(session.subject)
        return completion

    @staticmethod
    def mark_session_skip(session: StudySession, *, remarks=""):
        session.status = "skipped"
        session.save(update_fields=["status", "updated_at"])
        completion, _ = StudySessionCompletion.objects.update_or_create(
            study_session=session,
            user=session.user,
            defaults={
                "completed_at": None,
                "actual_minutes": 0,
                "completion_status": "skipped",
                "remarks": remarks,
            },
        )
        ProgressService.sync_subject_progress_for_subject(session.subject)
        return completion

    @staticmethod
    def mark_assessment_complete(assessment: Assessment):
        assessment.status = "completed"
        assessment.is_locked_after_completion = True
        assessment.save(update_fields=["status", "is_locked_after_completion", "updated_at"])
        AssessmentProgress.objects.update_or_create(
            assessment=assessment,
            user=assessment.user,
            defaults={"progress_percent": 100, "status": "completed"},
        )
        ProgressService.sync_subject_progress_for_subject(assessment.subject)
        return assessment

    @staticmethod
    def overview(user):
        subject_progress = SubjectProgress.objects.filter(user=user)
        total_subjects = subject_progress.count()
        total_completion_rate = round(sum(item.completion_rate for item in subject_progress) / total_subjects, 2) if total_subjects else 0
        total_study_hours = round(sum(item.total_completed_minutes for item in subject_progress) / 60, 2)
        completed_assessments = Assessment.objects.filter(user=user, status="completed").count()
        pending_assessments = Assessment.objects.filter(user=user, status__in=["pending", "in_progress", "overdue"]).count()
        return {
            "totalSubjects": total_subjects,
            "averageCompletionRate": total_completion_rate,
            "totalStudyHours": total_study_hours,
            "completedAssessments": completed_assessments,
            "pendingAssessments": pending_assessments,
        }

    @staticmethod
    def weekly_metrics(user):
        start = timezone.now().date() - timedelta(days=6)
        rows = []
        for offset in range(7):
            current_date = start + timedelta(days=offset)
            sessions = StudySession.objects.filter(user=user, session_date=current_date, status="completed")
            rows.append(
                {
                    "date": current_date.isoformat(),
                    "day": current_date.strftime("%a"),
                    "completedSessions": sessions.count(),
                    "studyMinutes": sessions.aggregate(total=Sum("duration_minutes"))["total"] or 0,
                }
            )
        return rows
