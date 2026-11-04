import re

from rest_framework import serializers

from .models import (
    PAYMENT_CHOICES,
    STATUS_REJECTED,
    ExamApplication,
    ExamCenter,
    ExamConfig,
    normalize_phone,
)

PHONE_RE = re.compile(r"^01[3-9]\d{8}$")


def clean_phone(value: str, label: str = "মোবাইল নম্বর") -> str:
    phone = normalize_phone(value)
    if not PHONE_RE.match(phone):
        raise serializers.ValidationError(f"সঠিক {label} দিন (01XXXXXXXXX)।")
    return phone


class ExamCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamCenter
        fields = ["id", "name", "location", "short_name", "order", "is_active"]


class ExamConfigSerializer(serializers.ModelSerializer):
    accepting = serializers.BooleanField(read_only=True)
    deadline_passed = serializers.BooleanField(read_only=True)
    centers = serializers.SerializerMethodField()

    class Meta:
        model = ExamConfig
        fields = [
            "title", "short_title", "year", "application_prefix", "exam_date", "exam_time",
            "deadline", "fee", "bkash_number", "nagad_number", "rocket_number",
            "applications_open", "show_home_banner", "admit_download_open",
            "roll_start_8", "roll_start_9", "roll_start_10", "contacts",
            "accepting", "deadline_passed", "centers", "updated_at",
        ]
        read_only_fields = ["updated_at"]

    def get_centers(self, obj):
        return ExamCenterSerializer(ExamCenter.objects.filter(is_active=True), many=True).data


class ApplicationCreateSerializer(serializers.ModelSerializer):
    """Public online application. Payment is always a mobile-wallet Send Money."""

    phone = serializers.CharField(max_length=20)  # normalized to 11 digits in validate_phone
    payment_method = serializers.ChoiceField(choices=["bkash", "nagad", "rocket"])
    sender_number = serializers.CharField(max_length=20)
    trx_id = serializers.CharField(max_length=40)
    photo_url = serializers.URLField(max_length=600)

    class Meta:
        model = ExamApplication
        fields = [
            "name_bn", "name_en", "mother_name", "father_name", "phone", "photo_url",
            "class_level", "institution", "village", "union", "center",
            "payment_method", "sender_number", "trx_id",
        ]

    def validate_phone(self, value):
        return clean_phone(value)

    def validate_sender_number(self, value):
        return clean_phone(value, "পাঠানো নম্বর")

    def validate_name_en(self, value):
        return value.strip().upper()

    def validate_trx_id(self, value):
        value = re.sub(r"\s", "", value).upper()
        if len(value) < 6:
            raise serializers.ValidationError("সঠিক Transaction ID দিন।")
        return value

    def validate_center(self, value):
        if not value.is_active:
            raise serializers.ValidationError("এই কেন্দ্রটি এখন নেওয়া হচ্ছে না।")
        return value

    def validate(self, attrs):
        config: ExamConfig = self.context["config"]
        if ExamApplication.objects.filter(
            exam_year=config.year,
            payment_method=attrs["payment_method"],
            trx_id=attrs["trx_id"],
        ).exists():
            raise serializers.ValidationError(
                {"trx_id": "এই Transaction ID দিয়ে আগেই একটি আবেদন জমা হয়েছে।"}
            )
        for key in ("name_bn", "mother_name", "father_name", "institution", "village", "union"):
            attrs[key] = attrs[key].strip()
        return attrs


class ApplicationStatusSerializer(serializers.ModelSerializer):
    """What a student sees after looking up their application (number + phone)."""

    center = ExamCenterSerializer(read_only=True)
    class_label = serializers.CharField(source="get_class_level_display", read_only=True)
    payment_label = serializers.CharField(source="get_payment_method_display", read_only=True)
    admit_available = serializers.SerializerMethodField()
    note = serializers.SerializerMethodField()

    class Meta:
        model = ExamApplication
        fields = [
            "application_no", "name_bn", "name_en", "photo_url", "class_level", "class_label",
            "institution", "center", "payment_method", "payment_label", "trx_id", "amount",
            "status", "serial_no", "roll_no", "admit_available", "note", "created_at",
        ]

    def get_admit_available(self, obj):
        return obj.admit_ready and self.context["config"].admit_download_open

    def get_note(self, obj):
        # Only a rejection reason is meant for the student; other notes are internal.
        return obj.note if obj.status == STATUS_REJECTED else ""


class ApplicationAdminSerializer(serializers.ModelSerializer):
    center_name = serializers.CharField(source="center.name", read_only=True)
    center_short = serializers.SerializerMethodField()
    class_label = serializers.CharField(source="get_class_level_display", read_only=True)
    payment_label = serializers.CharField(source="get_payment_method_display", read_only=True)
    photo_url = serializers.URLField(max_length=600, required=False, allow_blank=True)
    phone = serializers.CharField(max_length=20)
    sender_number = serializers.CharField(max_length=20, required=False, allow_blank=True)
    payment_method = serializers.ChoiceField(
        choices=[c for c, _ in PAYMENT_CHOICES], required=False, default="offline"
    )

    class Meta:
        model = ExamApplication
        fields = [
            "id", "exam_year", "application_no", "name_bn", "name_en", "mother_name",
            "father_name", "phone", "photo_url", "class_level", "class_label", "institution",
            "village", "union", "upazila", "district", "center", "center_name", "center_short",
            "payment_method", "payment_label", "sender_number", "trx_id", "amount", "status",
            "note", "serial_no", "roll_no", "verified_at", "admit_downloaded_at",
            "created_at", "updated_at",
        ]
        read_only_fields = [
            "id", "exam_year", "application_no", "status", "serial_no", "roll_no",
            "verified_at", "admit_downloaded_at", "created_at", "updated_at",
        ]

    def get_center_short(self, obj):
        return obj.center.short_name or obj.center.name

    def validate_phone(self, value):
        return clean_phone(value)

    def validate_sender_number(self, value):
        return clean_phone(value, "পাঠানো নম্বর") if value else ""

    def validate_name_en(self, value):
        return value.strip().upper()

    def validate_trx_id(self, value):
        return re.sub(r"\s", "", value).upper()
