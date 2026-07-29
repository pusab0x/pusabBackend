from django.db.models import Case, IntegerField, When
from rest_framework import viewsets

from config.permissions import IsAdminOrReadOnly

from .models import DESIGNATION_ORDER, EcMember, LeaderMessage
from .serializers import EcMemberSerializer, LeaderMessageSerializer

# Case/When ladder mirroring DESIGNATION_ORDER, for ordering by designation
# hierarchy in the database rather than alphabetically. Unmatched roles (not
# in the list) fall through to the default, sorting after every known rank.
_ROLE_RANK_CASES = [
    When(role__iexact=role, then=i) for i, role in enumerate(DESIGNATION_ORDER)
]


class EcMemberViewSet(viewsets.ModelViewSet):
    queryset = EcMember.objects.all()
    serializer_class = EcMemberSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        year = self.request.query_params.get("year")
        if year:
            qs = qs.filter(year=year, is_convening=False)
        if self.request.query_params.get("current") == "true":
            qs = qs.filter(is_current=True)
        if self.request.query_params.get("convening") == "true":
            qs = qs.filter(is_convening=True)
        qs = qs.annotate(
            role_rank=Case(
                *_ROLE_RANK_CASES,
                default=len(DESIGNATION_ORDER),
                output_field=IntegerField(),
            )
        ).order_by("-year", "role_rank", "name")
        return qs


class LeaderMessageViewSet(viewsets.ModelViewSet):
    """President / General Secretary messages — looked up by role."""

    queryset = LeaderMessage.objects.all()
    serializer_class = LeaderMessageSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "role"
