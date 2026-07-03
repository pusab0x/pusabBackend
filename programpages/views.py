from rest_framework import viewsets

from config.permissions import IsAdminOrReadOnly

from .models import ProgramPage
from .serializers import ProgramPageSerializer


class ProgramPageViewSet(viewsets.ModelViewSet):
    """Program pages, looked up by slug (e.g. /api/program-pages/reunion/)
    rather than numeric id, so the frontend route and API line up."""

    queryset = ProgramPage.objects.prefetch_related(
        "objectives", "stats", "gallery", "testimonials"
    )
    serializer_class = ProgramPageSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "slug"
    lookup_value_regex = "[^/]+"
