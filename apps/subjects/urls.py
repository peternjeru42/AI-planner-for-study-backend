from rest_framework.routers import DefaultRouter

from apps.subjects.views import SubjectViewSet


router = DefaultRouter()
router.register("", SubjectViewSet, basename="subject")

urlpatterns = router.urls
