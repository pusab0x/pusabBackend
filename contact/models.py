from django.db import models


class ContactMessage(models.Model):
    """A membership inquiry / contact message from the public form."""

    BLOOD_GROUP_CHOICES = [
        ("A+", "A+"), ("A-", "A-"),
        ("B+", "B+"), ("B-", "B-"),
        ("AB+", "AB+"), ("AB-", "AB-"),
        ("O+", "O+"), ("O-", "O-"),
    ]

    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=40, blank=True)
    father_name = models.CharField(max_length=150, blank=True)
    mother_name = models.CharField(max_length=150, blank=True)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, blank=True)
    subject = models.CharField(max_length=200, blank=True)
    university = models.CharField(max_length=200, blank=True)
    session = models.CharField(max_length=40, blank=True)
    union_name = models.CharField(max_length=150, blank=True)
    village = models.CharField(max_length=150, blank=True)
    school = models.CharField(max_length=200, blank=True)
    college = models.CharField(max_length=200, blank=True)
    message = models.TextField(blank=True)
    # email kept optional for backward compatibility
    email = models.EmailField(blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} · {self.phone}"
