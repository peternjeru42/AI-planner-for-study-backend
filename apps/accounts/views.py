from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from apps.accounts.serializers import (
    AuthPayloadSerializer,
    LoginSerializer,
    LogoutSerializer,
    ProfileUpdateSerializer,
    RegisterSerializer,
    StudentProfileSerializer,
    UserSerializer,
)
from apps.accounts.services import AuthService
from common.utils import api_success


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = AuthService.register_user(
            full_name=serializer.validated_data["fullName"],
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )
        payload = AuthPayloadSerializer.from_user(user)
        return api_success(payload, "Account created successfully.", 201)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = AuthService.login_user(**serializer.validated_data)
        return api_success(AuthPayloadSerializer.from_user(user), "Login successful.")


class LogoutView(APIView):
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        AuthService.logout_user(refresh_token=serializer.validated_data["refresh"])
        return api_success({}, "Logout successful.")


class MeView(APIView):
    def get(self, request):
        profile = getattr(request.user, "student_profile", None)
        return api_success(
            {
                "user": UserSerializer(request.user).data,
                "profile": StudentProfileSerializer(profile).data if profile else None,
            },
            "Profile fetched successfully.",
        )


class ProfileView(APIView):
    def put(self, request):
        serializer = ProfileUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = AuthService.update_profile(user=request.user, payload=serializer.validated_data)
        return api_success(
            {
                "user": UserSerializer(user).data,
                "profile": StudentProfileSerializer(user.student_profile).data,
            },
            "Profile updated successfully.",
        )


class ForgotPasswordSimulatedView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        return api_success({"simulated": True}, "Password reset simulated successfully.")

# Create your views here.
