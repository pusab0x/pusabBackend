from rest_framework.routers import DefaultRouter

from .views import PageHeroViewSet

router = DefaultRouter()
router.register("page-heroes", PageHeroViewSet, basename="page-heroes")

urlpatterns = router.urls
