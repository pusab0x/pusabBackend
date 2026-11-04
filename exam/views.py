from django.db import IntegrityError
from django.db.models import Count, Q, Sum
from django.utils import timezone
from rest_framework import generics, permissions, status, throttling, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from config.permissions import IsAdminOrReadOnly

from . import services
from .models import (
    STATUS_PENDING,
    STATUS_REJECTED,
    STATUS_VERIFIED,
    ExamApplication,
    ExamCenter,
    ExamConfig,
    normalize_phone,
)
from .serializers import (
    ApplicationAdminSerializer,
    ApplicationCreateSerializer,
    ApplicationStatusSerializer,
    ExamCenterSerializer,
    ExamConfigSerializer,
)


class ExamApplyThrottle(throttling.AnonRateThrottle):
    scope = "exam_apply"


class ExamStatusThrottle(throttling.AnonRateThrottle):
    scope = "exam_status"


class ExamConfigView(generics.RetrieveUpdateAPIView):
    """Current exam edition — read publicly, edited by admins."""

    serializer_class = ExamConfigSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_object(self):
        return ExamConfig.load()


class ExamCenterViewSet(viewsets.ModelViewSet):
    serializer_class = ExamCenterSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = None

    def get_queryset(self):
        qs = ExamCenter.objects.all()
        if not (self.request.user and self.request.user.is_staff):
            qs = qs.filter(is_active=True)
        return qs

    def perform_destroy(self, instance):
        if instance.applications.exists():
            raise ValidationError(
                {"detail": "এই কেন্দ্রে আবেদন আছে — মুছে না ফেলে নিষ্ক্রিয় করুন।"}
            )
        instance.delete()


class ApplyView(APIView):
    """Public: submit an online application."""

    permission_classes = [permissions.AllowAny]
    throttle_classes = [ExamApplyThrottle]

    def post(self, request):
        if request.data.get("website"):  # honeypot
            raise ValidationError({"detail": "Invalid submission."})
        config = ExamConfig.load()
        if not config.accepting:
            raise ValidationError({"detail": "অনলাইন আবেদন এখন বন্ধ আছে।"})
        serializer = ApplicationCreateSerializer(data=request.data, context={"config": config})
        serializer.is_valid(raise_exception=True)
        try:
            app = services.create_application(config, amount=config.fee, **serializer.validated_data)
        except IntegrityError:
            raise ValidationError(
                {"trx_id": "এই Transaction ID দিয়ে আগেই একটি আবেদন জমা হয়েছে।"}
            )
        data = ApplicationStatusSerializer(app, context={"config": config}).data
        return Response(data, status=status.HTTP_201_CREATED)


class StatusView(APIView):
    """Public: look up an application by its number + the student's phone.
    POST so the phone number stays out of URLs and access logs."""

    permission_classes = [permissions.AllowAny]
    throttle_classes = [ExamStatusThrottle]

    def post(self, request):
        number = str(request.data.get("application_no", "")).strip().upper()
        phone = normalize_phone(str(request.data.get("phone", "")))
        app = (
            ExamApplication.objects.select_related("center")
            .filter(application_no=number, phone=phone)
            .first()
        )
        if not number or not app:
            return Response(
                {"detail": "আবেদন নম্বর ও মোবাইল নম্বর মেলেনি। আবার দেখে লিখুন।"},
                status=status.HTTP_404_NOT_FOUND,
            )
        config = ExamConfig.load()
        serializer = ApplicationStatusSerializer(app, context={"config": config})
        if request.data.get("mark_downloaded") and serializer.data["admit_available"]:
            if not app.admit_downloaded_at:
                app.admit_downloaded_at = timezone.now()
                app.save(update_fields=["admit_downloaded_at"])
        return Response(serializer.data)


class AdminPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = "page_size"
    max_page_size = 5000


class ApplicationAdminViewSet(viewsets.ModelViewSet):
    """Admin: review applications, verify payments, assign rolls."""

    serializer_class = ApplicationAdminSerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = AdminPagination

    def get_queryset(self):
        params = self.request.query_params
        qs = ExamApplication.objects.select_related("center")
        year = params.get("year") or ExamConfig.load().year
        qs = qs.filter(exam_year=year)
        if params.get("status"):
            qs = qs.filter(status=params["status"])
        if params.get("class_level"):
            qs = qs.filter(class_level=params["class_level"])
        if params.get("center"):
            qs = qs.filter(center_id=params["center"])
        if params.get("has_roll") == "true":
            qs = qs.filter(roll_no__isnull=False)
        if q := params.get("q", "").strip():
            qs = qs.filter(
                Q(name_bn__icontains=q)
                | Q(name_en__icontains=q)
                | Q(phone__icontains=normalize_phone(q) or q)
                | Q(trx_id__icontains=q)
                | Q(application_no__icontains=q)
            )
        if params.get("order") == "roll":
            qs = qs.order_by("class_level", "roll_no")
        return qs

    def perform_create(self, serializer):
        """Offline application taken in person — counts as already paid."""
        config = ExamConfig.load()
        data = dict(serializer.validated_data)
        data.setdefault("payment_method", "offline")
        data.setdefault("amount", config.fee)
        try:
            app = services.create_application(config, **data)
        except IntegrityError:
            raise ValidationError({"trx_id": "এই Transaction ID আগেই ব্যবহার হয়েছে।"})
        services.verify(app)
        serializer.instance = app

    def perform_update(self, serializer):
        try:
            serializer.save()
        except IntegrityError:
            raise ValidationError({"trx_id": "এই Transaction ID আগেই ব্যবহার হয়েছে।"})

    @action(detail=True, methods=["post"])
    def verify(self, request, pk=None):
        app = services.verify(self.get_object(), note=request.data.get("note", ""))
        return Response(self.get_serializer(app).data)

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        note = str(request.data.get("note", "")).strip()
        if not note:
            raise ValidationError({"note": "বাতিলের কারণ লিখুন।"})
        app = services.reject(self.get_object(), note)
        return Response(self.get_serializer(app).data)

    @action(detail=True, methods=["post"])
    def reset(self, request, pk=None):
        """Move back to 'pending' (e.g. a mistaken rejection)."""
        app = self.get_object()
        app.status = STATUS_PENDING
        app.roll_no = app.serial_no = app.verified_at = None
        app.save(update_fields=["status", "roll_no", "serial_no", "verified_at", "updated_at"])
        return Response(self.get_serializer(app).data)

    @action(detail=True, methods=["post"], url_path="assign-roll")
    def assign_roll(self, request, pk=None):
        app = self.get_object()
        if app.status != STATUS_VERIFIED:
            raise ValidationError({"detail": "আগে পেমেন্ট নিশ্চিত করুন।"})
        self._assign(only=app)
        app.refresh_from_db()
        return Response(self.get_serializer(app).data)

    @action(detail=False, methods=["post"], url_path="assign-rolls")
    def assign_rolls(self, request):
        assigned = self._assign()
        return Response({"assigned": assigned})

    def _assign(self, only=None) -> int:
        try:
            return services.assign_rolls(ExamConfig.load(), only=only)
        except IntegrityError:
            raise ValidationError(
                {"detail": "রোল নম্বর মিলে যাচ্ছে — শ্রেণিভিত্তিক রোল শুরুর নম্বরগুলো আলাদা রাখুন।"}
            )

    @action(detail=False, methods=["get"])
    def stats(self, request):
        config = ExamConfig.load()
        qs = ExamApplication.objects.filter(exam_year=config.year)
        agg = qs.aggregate(
            total=Count("id"),
            pending=Count("id", filter=Q(status=STATUS_PENDING)),
            verified=Count("id", filter=Q(status=STATUS_VERIFIED)),
            rejected=Count("id", filter=Q(status=STATUS_REJECTED)),
            collected=Sum("amount", filter=Q(status=STATUS_VERIFIED)),
            with_roll=Count("id", filter=Q(roll_no__isnull=False)),
            downloaded=Count("id", filter=Q(admit_downloaded_at__isnull=False)),
        )
        agg["collected"] = agg["collected"] or 0
        agg["verified_by_class"] = {
            str(c): qs.filter(status=STATUS_VERIFIED, class_level=c).count() for c in (8, 9, 10)
        }
        return Response(agg)
