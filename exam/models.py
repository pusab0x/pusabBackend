import datetime
import re

from django.db import models
from django.db.models import Q
from django.utils import timezone

CLASS_CHOICES = [(8, "অষ্টম"), (9, "নবম"), (10, "দশম")]

PAYMENT_CHOICES = [
    ("bkash", "বিকাশ"),
    ("nagad", "নগদ"),
    ("rocket", "রকেট"),
    ("offline", "অফলাইন"),  # paid in person; added by an admin
]

STATUS_PENDING = "pending"
STATUS_VERIFIED = "verified"
STATUS_REJECTED = "rejected"
STATUS_CHOICES = [
    (STATUS_PENDING, "যাচাই বাকি"),
    (STATUS_VERIFIED, "যাচাই সম্পন্ন"),
    (STATUS_REJECTED, "বাতিল"),
]

_BN_DIGITS = str.maketrans("০১২৩৪৫৬৭৮৯", "0123456789")


def normalize_phone(value: str) -> str:
    """Accept Bengali digits, spaces, dashes and a +88 prefix; return 01XXXXXXXXX."""
    digits = re.sub(r"\D", "", (value or "").translate(_BN_DIGITS))
    if digits.startswith("88") and len(digits) == 13:
        digits = digits[2:]
    return digits


def default_contacts():
    return [
        {"name": "মানিক চৌধুরী", "role": "সভাপতি, পুসাব", "phone": "01765597615"},
        {"name": "মুহাম্মদ বাবর", "role": "সাধারণ সম্পাদক, পুসাব", "phone": "01984821716"},
    ]


class ExamConfig(models.Model):
    """Singleton: the current edition of the PUSAB scholarship exam."""

    title = models.CharField(max_length=200, default="৮ম পুসাব মেধাবৃত্তি পরীক্ষা- ২০২৫")
    short_title = models.CharField(max_length=120, default="৮ম পুসাব মেধাবৃত্তি")
    year = models.PositiveIntegerField(default=2025)
    application_prefix = models.CharField(max_length=20, default="PUSAB-25")
    exam_date = models.DateField(null=True, blank=True, default=datetime.date(2025, 12, 26))
    exam_time = models.CharField(max_length=60, default="সকাল ১০.০০ টা")
    deadline = models.DateField(null=True, blank=True)  # last day, inclusive (Asia/Dhaka)
    fee = models.PositiveIntegerField(default=50)
    bkash_number = models.CharField(max_length=20, blank=True)
    nagad_number = models.CharField(max_length=20, blank=True)
    rocket_number = models.CharField(max_length=20, blank=True)
    applications_open = models.BooleanField(default=True)
    show_home_banner = models.BooleanField(default=True)
    admit_download_open = models.BooleanField(default=False)
    roll_start_8 = models.PositiveIntegerField(default=8001)
    roll_start_9 = models.PositiveIntegerField(default=9001)
    roll_start_10 = models.PositiveIntegerField(default=1001)
    contacts = models.JSONField(default=default_contacts, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Exam settings"
        verbose_name_plural = "Exam settings"

    def save(self, *args, **kwargs):
        self.pk = 1  # enforce a single row
        super().save(*args, **kwargs)

    @classmethod
    def load(cls) -> "ExamConfig":
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    @property
    def deadline_passed(self) -> bool:
        return bool(self.deadline and timezone.localdate() > self.deadline)

    @property
    def accepting(self) -> bool:
        return self.applications_open and not self.deadline_passed

    def roll_start(self, class_level: int) -> int:
        return getattr(self, f"roll_start_{class_level}")

    def __str__(self):
        return self.title


class ExamCenter(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=120, blank=True)
    short_name = models.CharField(max_length=60, blank=True)  # for tight table cells
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.name}, {self.location}" if self.location else self.name


class ExamApplication(models.Model):
    exam_year = models.PositiveIntegerField(db_index=True)
    application_no = models.CharField(max_length=30, unique=True, blank=True, null=True)

    name_bn = models.CharField(max_length=150)
    name_en = models.CharField(max_length=150)
    mother_name = models.CharField(max_length=150)
    father_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=11)
    photo_url = models.URLField(max_length=600, blank=True)

    class_level = models.PositiveSmallIntegerField(choices=CLASS_CHOICES)
    institution = models.CharField(max_length=200)
    village = models.CharField(max_length=120)
    union = models.CharField(max_length=120)
    upazila = models.CharField(max_length=120, default="বিশ্বম্ভরপুর")
    district = models.CharField(max_length=120, default="সুনামগঞ্জ")
    center = models.ForeignKey(ExamCenter, on_delete=models.PROTECT, related_name="applications")

    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    sender_number = models.CharField(max_length=11, blank=True)
    trx_id = models.CharField(max_length=40, blank=True)
    amount = models.PositiveIntegerField(default=0)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING, db_index=True)
    note = models.TextField(blank=True)  # admin note / rejection reason (shown to the student)
    serial_no = models.PositiveIntegerField(null=True, blank=True)
    roll_no = models.PositiveIntegerField(null=True, blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    admit_downloaded_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at", "-id"]
        constraints = [
            # One payment can only pay for one application.
            models.UniqueConstraint(
                fields=["exam_year", "payment_method", "trx_id"],
                condition=~Q(trx_id=""),
                name="exam_unique_trx_per_year",
            ),
            models.UniqueConstraint(
                fields=["exam_year", "roll_no"],
                condition=Q(roll_no__isnull=False),
                name="exam_unique_roll_per_year",
            ),
            models.UniqueConstraint(
                fields=["exam_year", "serial_no"],
                condition=Q(serial_no__isnull=False),
                name="exam_unique_serial_per_year",
            ),
        ]

    def __str__(self):
        return f"{self.application_no or 'new'} — {self.name_en}"

    @property
    def admit_ready(self) -> bool:
        return self.status == STATUS_VERIFIED and self.roll_no is not None
