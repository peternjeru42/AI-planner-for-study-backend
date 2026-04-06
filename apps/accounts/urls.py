from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.accounts.views import ForgotPasswordSimulatedView, LoginView, LogoutView, MeView, ProfileView, RegisterView


urlpatterns = [
    path("register/", RegisterView.as_view(), name="auth-register"),
    path("login/", LoginView.as_view(), name="auth-login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("me/", MeView.as_view(), name="auth-me"),
    path("profile/", ProfileView.as_view(), name="auth-profile"),
    path("logout/", LogoutView.as_view(), name="auth-logout"),
    path("forgot-password-simulated/", ForgotPasswordSimulatedView.as_view(), name="auth-forgot-password-simulated"),
]
