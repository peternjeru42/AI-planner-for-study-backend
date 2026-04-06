from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.models import StudentProfile, User


class AuthService:
    @staticmethod
    @transaction.atomic
    def register_user(*, full_name: str, email: str, password: str) -> User:
        user = User.objects.create_user(
            email=email,
            password=password,
            full_name=full_name,
            role="student",
            is_verified=True,
        )
        StudentProfile.objects.create(user=user)
        return user

    @staticmethod
    def login_user(*, email: str, password: str) -> User:
        user = authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed("Invalid credentials.")
        return user

    @staticmethod
    def logout_user(*, refresh_token: str) -> None:
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as exc:  # noqa: BLE001
            raise ValidationError({"refresh": ["Invalid refresh token."]}) from exc

    @staticmethod
    @transaction.atomic
    def update_profile(*, user: User, payload: dict) -> User:
        profile, _ = StudentProfile.objects.get_or_create(user=user)
        user_fields = {
            "name": "full_name",
            "username": "username",
        }
        profile_fields = {
            "courseName": "course_name",
            "yearOfStudy": "year_of_study",
            "institutionName": "institution_name",
            "timezone": "timezone",
            "startTime": "preferred_study_start_time",
            "endTime": "preferred_study_end_time",
            "sessionLength": "preferred_session_length_minutes",
            "breakLength": "preferred_break_length_minutes",
            "maxSessionsPerDay": "max_sessions_per_day",
            "weekendAvailable": "weekend_available",
            "enableInAppNotifications": "enable_in_app_notifications",
            "enableEmailNotificationsSimulated": "enable_email_notifications_simulated",
            "darkMode": "dark_mode",
        }
        for source, target in user_fields.items():
            if source in payload:
                setattr(user, target, payload[source])
        for source, target in profile_fields.items():
            if source in payload:
                setattr(profile, target, payload[source])
        user.save()
        profile.save()
        return user
