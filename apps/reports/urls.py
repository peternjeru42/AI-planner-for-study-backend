from django.urls import path

from apps.reports.views import CompletionTrendReportView, DeadlinesBySubjectReportView, ExportCSVReportView, MonthlyReportView, StudyHoursBySubjectReportView, WeeklyReportView


urlpatterns = [
    path("weekly/", WeeklyReportView.as_view(), name="reports-weekly"),
    path("monthly/", MonthlyReportView.as_view(), name="reports-monthly"),
    path("completion-trend/", CompletionTrendReportView.as_view(), name="reports-completion-trend"),
    path("study-hours-by-subject/", StudyHoursBySubjectReportView.as_view(), name="reports-study-hours-by-subject"),
    path("deadlines-by-subject/", DeadlinesBySubjectReportView.as_view(), name="reports-deadlines-by-subject"),
    path("export/csv/", ExportCSVReportView.as_view(), name="reports-export-csv"),
]
