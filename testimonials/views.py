from rest_framework import viewsets

from config.permissions import IsAdminOrReadOnly

from .models import Testimonial
from .serializers import TestimonialSerializer


class TestimonialViewSet(viewsets.ModelViewSet):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        featured = self.request.query_params.get("is_featured")
        if featured is not None:
            qs = qs.filter(is_featured=featured.lower() in ("1", "true", "yes"))
        return qs
