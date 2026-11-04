"""Root URL configuration for the PUSAB API."""
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts.views import UserViewSet

router = DefaultRouter()
router.register("users", UserViewSet, basename="users")

urlpatterns = [
    path("django-admin/", admin.site.urls),  # built-in admin (optional, not the public dashboard)
    # Auth (JWT)
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/auth/", include("accounts.urls")),
    # Admin user management
    path("api/", include(router.urls)),
    # Domain APIs
    path("api/", include("gallery.urls")),
    path("api/", include("publicity.urls")),
    path("api/", include("committee.urls")),
    path("api/", include("programs.urls")),
    path("api/", include("contact.urls")),
    path("api/", include("siteconfig.urls")),
    path("api/", include("felicitation.urls")),
    path("api/", include("programpages.urls")),
    path("api/", include("testimonials.urls")),
    path("api/", include("pagehero.urls")),
    path("api/", include("exam.urls")),
]
