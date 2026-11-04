from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    ApplicationAdminViewSet,
    ApplyView,
    ExamCenterViewSet,
    ExamConfigView,
    StatusView,
)

router = DefaultRouter()
router.register("exam/centers", ExamCenterViewSet, basename="exam-centers")
router.register("exam/applications", ApplicationAdminViewSet, basename="exam-applications")

urlpatterns = [
    path("exam/config/", ExamConfigView.as_view(), name="exam-config"),
    path("exam/apply/", ApplyView.as_view(), name="exam-apply"),
    path("exam/status/", StatusView.as_view(), name="exam-status"),
] + router.urls
