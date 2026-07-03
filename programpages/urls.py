from rest_framework.routers import DefaultRouter

from .views import ProgramPageViewSet

router = DefaultRouter()
router.register("program-pages", ProgramPageViewSet, basename="program-pages")

urlpatterns = router.urls
