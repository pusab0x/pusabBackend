from django.db import models


class Testimonial(models.Model):
    """A community voice/testimonial shown in the homepage carousel."""

    name = models.CharField(max_length=150)
    role = models.CharField(max_length=200, blank=True)  # e.g. "Scholarship Recipient 2023"
    quote = models.TextField()
    photo_url = models.URLField(max_length=600, blank=True)
    program = models.CharField(max_length=150, blank=True)  # optional free-text program reference
    is_featured = models.BooleanField(default=True)  # controls homepage carousel visibility
    order = models.PositiveIntegerField(default=0)  # controls carousel ordering
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return f"{self.name} ({self.role})" if self.role else self.name
