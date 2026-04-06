from rest_framework.views import APIView

from apps.dashboard.services import DashboardService
from common.permissions import IsAdmin, IsStudent
from common.utils import api_success


class StudentDashboardView(APIView):
    permission_classes = [IsStudent]

    def get(self, request):
        return api_success(DashboardService.student_dashboard(request.user), "Student dashboard fetched successfully.")


class AdminDashboardView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        return api_success(DashboardService.admin_dashboard(), "Admin dashboard fetched successfully.")

# Create your views here.
