from rest_framework.views import APIView

from apps.assessments.models import Assessment
from apps.assessments.serializers import AssessmentSerializer
from apps.planner.models import StudySession
from apps.planner.serializers import StudySessionSerializer
from apps.progress.models import SubjectProgress
from apps.progress.serializers import SubjectProgressSerializer
from apps.progress.services import ProgressService
from common.permissions import IsStudent
from common.utils import api_success


class ProgressOverviewView(APIView):
    permission_classes = [IsStudent]

    def get(self, request):
        ProgressService.sync_all_subject_progress(request.user)
        return api_success(ProgressService.overview(request.user), "Progress overview fetched successfully.")


class ProgressSubjectsView(APIView):
    permission_classes = [IsStudent]

    def get(self, request):
        ProgressService.sync_all_subject_progress(request.user)
        queryset = SubjectProgress.objects.filter(user=request.user).select_related("subject")
        return api_success(SubjectProgressSerializer(queryset, many=True).data, "Subject progress fetched successfully.")


class ProgressWeeklyView(APIView):
    permission_classes = [IsStudent]

    def get(self, request):
        return api_success(ProgressService.weekly_metrics(request.user), "Weekly progress fetched successfully.")


class SessionCompleteView(APIView):
    permission_classes = [IsStudent]

    def post(self, request, session_id):
        session = StudySession.objects.get(id=session_id, user=request.user)
        ProgressService.mark_session_complete(session, actual_minutes=request.data.get("actualMinutes"), remarks=request.data.get("remarks", ""))
        return api_success(StudySessionSerializer(session).data, "Study session completed successfully.")


class SessionSkipView(APIView):
    permission_classes = [IsStudent]

    def post(self, request, session_id):
        session = StudySession.objects.get(id=session_id, user=request.user)
        ProgressService.mark_session_skip(session, remarks=request.data.get("remarks", ""))
        return api_success(StudySessionSerializer(session).data, "Study session skipped successfully.")


class AssessmentCompleteView(APIView):
    permission_classes = [IsStudent]

    def post(self, request, assessment_id):
        assessment = Assessment.objects.get(id=assessment_id, user=request.user)
        assessment = ProgressService.mark_assessment_complete(assessment)
        return api_success(AssessmentSerializer(assessment).data, "Assessment completed successfully.")

# Create your views here.
