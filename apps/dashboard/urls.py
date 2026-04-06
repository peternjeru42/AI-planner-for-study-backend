from django.urls import path

from apps.dashboard.views import AdminDashboardView, StudentDashboardView


urlpatterns = [
    path("student/", StudentDashboardView.as_view(), name="dashboard-student"),
    path("admin/", AdminDashboardView.as_view(), name="dashboard-admin"),
]
