from rest_framework.routers import DefaultRouter

from apps.assessments.views import AssessmentViewSet


router = DefaultRouter()
router.register("", AssessmentViewSet, basename="assessment")

urlpatterns = router.urls
