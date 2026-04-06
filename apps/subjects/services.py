from apps.progress.models import SubjectProgress
from apps.subjects.models import Subject


class SubjectService:
    @staticmethod
    def create_subject(*, user, data: dict) -> Subject:
        return Subject.objects.create(user=user, **data)

    @staticmethod
    def subject_progress(subject: Subject):
        progress = SubjectProgress.objects.filter(subject=subject).first()
        if not progress:
            return {
                "subjectId": subject.id,
                "totalAssessments": subject.assessments.count(),
                "completedAssessments": 0,
                "completionRate": 0.0,
                "studyHours": 0.0,
            }
        return {
            "subjectId": subject.id,
            "totalAssessments": progress.total_assessments,
            "completedAssessments": progress.completed_assessments,
            "completionRate": round(progress.completion_rate, 2),
            "studyHours": round(progress.total_completed_minutes / 60, 2),
        }
