from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response

from config.permissions import IsAdminOrReadOnly

from .models import ProgramPage
from .serializers import ProgramPageSerializer


class ProgramPageViewSet(viewsets.ModelViewSet):
    """Program page editions, looked up by slug (e.g.
    /api/program-pages/reunion/) rather than numeric id, so the frontend
    route and API line up. Since a slug now has one row per year, GET
    accepts an optional ?year= query param and otherwise returns the
    latest year available for that slug. The response includes a `years`
    list of every edition year that exists, so the frontend/dashboard can
    offer a year switcher without a second request."""

    queryset = ProgramPage.objects.prefetch_related(
        "objectives", "info_items", "stats", "gallery", "testimonials", "webinars"
    )
    serializer_class = ProgramPageSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "slug"
    lookup_value_regex = "[^/]+"

    def get_object(self):
        slug = self.kwargs["slug"]
        qs = ProgramPage.objects.filter(slug=slug)
        year = self.request.query_params.get("year")
        if year:
            return get_object_or_404(qs, year=year)
        obj = qs.order_by("-year").first()
        if obj is None:
            raise Http404
        return obj

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        data = self.get_serializer(instance).data
        years = list(
            ProgramPage.objects.filter(slug=instance.slug)
            .order_by("-year")
            .values_list("year", flat=True)
        )
        data["years"] = years
        return Response(data)

