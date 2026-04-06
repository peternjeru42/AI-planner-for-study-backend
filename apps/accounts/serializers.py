from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.models import StudentProfile, User


class StudentProfileSerializer(serializers.ModelSerializer):
    userId = serializers.UUIDField(source="user_id", read_only=True)
    startTime = serializers.TimeField(source="preferred_study_start_time", format="%H:%M")
    endTime = serializers.TimeField(source="preferred_study_end_time", format="%H:%M")
    sessionLength = serializers.IntegerField(source="preferred_session_length_minutes")
    breakLength = serializers.IntegerField(source="preferred_break_length_minutes")
    maxSessionsPerDay = serializers.IntegerField(source="max_sessions_per_day")
    weekendAvailable = serializers.BooleanField(source="weekend_available")
    enableInAppNotifications = serializers.BooleanField(source="enable_in_app_notifications")
    enableEmailNotificationsSimulated = serializers.BooleanField(source="enable_email_notifications_simulated")
    darkMode = serializers.BooleanField(source="dark_mode")
    courseName = serializers.CharField(source="course_name")
    yearOfStudy = serializers.IntegerField(source="year_of_study")
    institutionName = serializers.CharField(source="institution_name")

    class Meta:
        model = StudentProfile
        fields = [
            "userId",
            "courseName",
            "yearOfStudy",
            "institutionName",
            "timezone",
            "startTime",
            "endTime",
            "sessionLength",
            "breakLength",
            "maxSessionsPerDay",
            "weekendAvailable",
            "enableInAppNotifications",
            "enableEmailNotificationsSimulated",
            "darkMode",
        ]


class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="full_name")
    enrollmentDate = serializers.DateTimeField(source="created_at", read_only=True)
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)
    isActive = serializers.BooleanField(source="is_active", read_only=True)
    isVerified = serializers.BooleanField(source="is_verified", read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "email",
            "username",
            "role",
            "isActive",
            "isVerified",
            "enrollmentDate",
            "createdAt",
            "updatedAt",
        ]


class RegisterSerializer(serializers.Serializer):
    fullName = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)
    passwordConfirm = serializers.CharField(write_only=True, min_length=6)

    def validate(self, attrs):
        if attrs["password"] != attrs["passwordConfirm"]:
            raise serializers.ValidationError({"passwordConfirm": ["Passwords do not match."]})
        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError({"email": ["A user with this email already exists."]})
        return attrs


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class ProfileUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, max_length=255)
    username = serializers.CharField(required=False, allow_blank=True, allow_null=True, max_length=150)
    courseName = serializers.CharField(required=False, allow_blank=True, max_length=255)
    yearOfStudy = serializers.IntegerField(required=False, min_value=1)
    institutionName = serializers.CharField(required=False, allow_blank=True, max_length=255)
    timezone = serializers.CharField(required=False, max_length=64)
    startTime = serializers.TimeField(required=False, input_formats=["%H:%M"])
    endTime = serializers.TimeField(required=False, input_formats=["%H:%M"])
    sessionLength = serializers.IntegerField(required=False, min_value=15)
    breakLength = serializers.IntegerField(required=False, min_value=5)
    maxSessionsPerDay = serializers.IntegerField(required=False, min_value=1)
    weekendAvailable = serializers.BooleanField(required=False)
    enableInAppNotifications = serializers.BooleanField(required=False)
    enableEmailNotificationsSimulated = serializers.BooleanField(required=False)
    darkMode = serializers.BooleanField(required=False)


class AuthPayloadSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UserSerializer()
    profile = StudentProfileSerializer(allow_null=True)

    @staticmethod
    def from_user(user: User):
        refresh = RefreshToken.for_user(user)
        profile = getattr(user, "student_profile", None)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": UserSerializer(user).data,
            "profile": StudentProfileSerializer(profile).data if profile else None,
        }
