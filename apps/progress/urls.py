from django.urls import path

from apps.progress.views import AssessmentCompleteView, ProgressOverviewView, ProgressSubjectsView, ProgressWeeklyView, SessionCompleteView, SessionSkipView


urlpatterns = [
    path("overview/", ProgressOverviewView.as_view(), name="progress-overview"),
    path("subjects/", ProgressSubjectsView.as_view(), name="progress-subjects"),
    path("weekly/", ProgressWeeklyView.as_view(), name="progress-weekly"),
    path("sessions/<uuid:session_id>/complete/", SessionCompleteView.as_view(), name="progress-session-complete"),
    path("sessions/<uuid:session_id>/skip/", SessionSkipView.as_view(), name="progress-session-skip"),
    path("assessments/<uuid:assessment_id>/complete/", AssessmentCompleteView.as_view(), name="progress-assessment-complete"),
]
