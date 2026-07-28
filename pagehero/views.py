from rest_framework import viewsets

from config.permissions import IsAdminOrReadOnly

from .models import PageHero
from .serializers import PageHeroSerializer


class PageHeroViewSet(viewsets.ModelViewSet):
    """Hero banner (title / lede / image(s)) for a page — looked up by page key."""

    queryset = PageHero.objects.prefetch_related("images").all()
    serializer_class = PageHeroSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "page"
