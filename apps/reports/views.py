from django.http import HttpResponse
from rest_framework.views import APIView

from apps.reports.services import ReportService
from common.permissions import IsStudent
from common.utils import api_success


class WeeklyReportView(APIView):
    permission_classes = [IsStudent]

    def get(self, request):
        snapshot = ReportService.weekly(request.user)
        return api_success(
            {
                "weekStart": snapshot.week_start.isoformat(),
                "tasksCompleted": snapshot.tasks_completed,
                "studyMinutesCompleted": snapshot.study_minutes_completed,
                "studyMinutesPlanned": snapshot.study_minutes_planned,
                "completionRate": snapshot.completion_rate,
                "overdueCount": snapshot.overdue_count,
            },
            "Weekly report fetched successfully.",
        )


class MonthlyReportView(APIView):
    permission_classes = [IsStudent]

    def get(self, request):
        return api_success(ReportService.monthly(request.user), "Monthly report fetched successfully.")


class CompletionTrendReportView(APIView):
    permission_classes = [IsStudent]

    def get(self, request):
        return api_success(ReportService.completion_trend(request.user), "Completion trend fetched successfully.")


class StudyHoursBySubjectReportView(APIView):
    permission_classes = [IsStudent]

    def get(self, request):
        return api_success(ReportService.study_hours_by_subject(request.user), "Study hours by subject fetched successfully.")


class DeadlinesBySubjectReportView(APIView):
    permission_classes = [IsStudent]

    def get(self, request):
        return api_success(ReportService.deadlines_by_subject(request.user), "Deadlines by subject fetched successfully.")


class ExportCSVReportView(APIView):
    permission_classes = [IsStudent]

    def get(self, request):
        content = ReportService.export_csv(request.user)
        response = HttpResponse(content, content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="studyflow-report.csv"'
        return response

# Create your views here.
