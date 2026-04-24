from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.accounts.models import StudentProfile, User


class OptionalJWTOrGuestAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        if header:
            return super().authenticate(request)

        if request.path in {"/", "/api/health/"} or request.path.startswith("/admin/"):
            return None

        user, _ = User.objects.get_or_create(
            email="guest@example.com",
            defaults={
                "full_name": "Guest Student",
                "role": "student",
                "is_verified": True,
            },
        )
        StudentProfile.objects.get_or_create(user=user)
        return (user, None)
