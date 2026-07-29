from django.db import models

# Default category offered when creating a new entry — admins may type any
# other category freely, this is just a sensible starting point.
DEFAULT_CATEGORY = "Achiever"


class FelicitationEntry(models.Model):
    """An honouree on the Felicitation & Freshers page — an achiever felicitated,
    a fresher welcomed, or any other admin-defined category, for a given year."""

    name = models.CharField(max_length=150)
    title = models.CharField(max_length=200, blank=True)  # achievement / institution
    category = models.CharField(max_length=60, default=DEFAULT_CATEGORY)  # free text, admin-defined
    year = models.PositiveIntegerField()
    image_url = models.URLField(max_length=600, blank=True)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-year", "category", "name"]
        verbose_name_plural = "Felicitation entries"

    def __str__(self):
        return f"{self.name} ({self.year})"
