"""Application numbering and roll/serial assignment for the scholarship exam."""
from django.db import IntegrityError, transaction
from django.db.models import Max
from django.utils import timezone

from .models import STATUS_REJECTED, STATUS_VERIFIED, ExamApplication, ExamConfig


def _last_number(prefix: str) -> int:
    """Highest sequence number already used with this prefix (deletions leave
    gaps, so counting rows would hand out a number that is still taken)."""
    highest = 0
    for no in ExamApplication.objects.filter(application_no__startswith=prefix).values_list(
        "application_no", flat=True
    ):
        tail = no[len(prefix):]
        if tail.isdigit():
            highest = max(highest, int(tail))
    return highest


def create_application(config: ExamConfig, **fields) -> ExamApplication:
    """Save a new application and give it the next number for this edition,
    e.g. PUSAB-25-0007. Retries if two submissions race for the same number."""
    prefix = f"{config.application_prefix}-"
    for _ in range(5):
        try:
            with transaction.atomic():
                app = ExamApplication.objects.create(exam_year=config.year, **fields)
                app.application_no = f"{prefix}{_last_number(prefix) + 1:04d}"
                app.save(update_fields=["application_no"])
                return app
        except IntegrityError as exc:
            # A duplicate TrxID is a real validation error, not a numbering race.
            if "trx" in str(exc).lower():
                raise
    raise IntegrityError("Could not allocate an application number.")


def assign_rolls(config: ExamConfig, only: ExamApplication | None = None) -> int:
    """Give every verified application without a roll a serial (ক্রমিক) and
    roll number, class by class, ordered by centre then submission time.
    Rolls continue after the highest already given in that class, starting
    at the class's configured roll_start. Returns how many were assigned."""
    year = config.year
    assigned = 0
    with transaction.atomic():
        year_apps = ExamApplication.objects.select_for_update().filter(exam_year=year)
        next_serial = (year_apps.aggregate(m=Max("serial_no"))["m"] or 0) + 1
        for class_level in (8, 9, 10):
            pending = year_apps.filter(
                class_level=class_level, status=STATUS_VERIFIED, roll_no__isnull=True
            ).order_by("center__order", "center_id", "created_at", "id")
            if only is not None:
                pending = pending.filter(pk=only.pk)
            if not pending.exists():
                continue
            used = year_apps.filter(class_level=class_level).aggregate(m=Max("roll_no"))["m"]
            next_roll = max(config.roll_start(class_level), (used or 0) + 1)
            for app in pending:
                app.roll_no = next_roll
                app.serial_no = next_serial
                app.save(update_fields=["roll_no", "serial_no", "updated_at"])
                next_roll += 1
                next_serial += 1
                assigned += 1
    return assigned


def verify(app: ExamApplication, note: str = "") -> ExamApplication:
    app.status = STATUS_VERIFIED
    app.verified_at = app.verified_at or timezone.now()
    if note:
        app.note = note
    app.save(update_fields=["status", "verified_at", "note", "updated_at"])
    return app


def reject(app: ExamApplication, note: str) -> ExamApplication:
    app.status = STATUS_REJECTED
    app.note = note
    # A rejected application no longer holds a seat.
    app.roll_no = None
    app.serial_no = None
    app.verified_at = None
    app.save(update_fields=["status", "note", "roll_no", "serial_no", "verified_at", "updated_at"])
    return app
