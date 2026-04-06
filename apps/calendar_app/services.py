from datetime import datetime, time

from django.utils import timezone


class CalendarService:
    @staticmethod
    def assessment_events(user, start_date, end_date):
        events = []
        for assessment in user.assessments.filter(due_date__range=(start_date, end_date)).select_related("subject"):
            if assessment.due_time:
                start = timezone.make_aware(datetime.combine(assessment.due_date, assessment.due_time))
            else:
                start = timezone.make_aware(datetime.combine(assessment.due_date, time(9, 0)))
            events.append(
                {
                    "id": str(assessment.id),
                    "title": assessment.title,
                    "type": "assessment",
                    "start": start.isoformat(),
                    "end": start.isoformat(),
                    "allDay": not bool(assessment.due_time),
                    "status": assessment.status.replace("_", "-"),
                    "subjectId": str(assessment.subject_id),
                    "assessmentId": str(assessment.id),
                    "color": assessment.subject.color_tag,
                }
            )
        return events

    @staticmethod
    def session_events(user, start_date, end_date):
        events = []
        for session in user.study_sessions.filter(session_date__range=(start_date, end_date)).select_related("subject"):
            start = timezone.make_aware(datetime.combine(session.session_date, session.start_time))
            end = timezone.make_aware(datetime.combine(session.session_date, session.end_time))
            events.append(
                {
                    "id": str(session.id),
                    "title": session.title,
                    "type": "study-session",
                    "start": start.isoformat(),
                    "end": end.isoformat(),
                    "allDay": False,
                    "status": session.status.replace("_", "-"),
                    "subjectId": str(session.subject_id),
                    "studySessionId": str(session.id),
                    "color": session.subject.color_tag,
                }
            )
        return events
