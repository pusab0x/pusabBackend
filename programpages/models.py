from django.db import models


class ProgramPage(models.Model):
    """One year's edition of a program's dedicated page (e.g. Annual Reunion
    2026, Annual Reunion 2025). Keyed by (slug, year) — slug matches the
    frontend route (/programs/<slug>) and the PROGRAMS entry in
    site-content.ts; year lets every field (title, overview, stats,
    gallery, ...) differ from one edition to the next."""

    slug = models.SlugField(max_length=60)
    year = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    tagline = models.CharField(max_length=300, blank=True)
    hero_image_url = models.URLField(max_length=600, blank=True)
    overview = models.TextField(blank=True)
    eligibility = models.TextField(blank=True)
    process = models.TextField(blank=True)
    schedule_note = models.CharField(max_length=300, blank=True)

    # Event info card (date/venue/time) shown alongside the overview.
    event_date = models.CharField(max_length=100, blank=True)
    venue = models.CharField(max_length=200, blank=True)
    event_time = models.CharField(max_length=100, blank=True)

    # Register / RSVP call-to-action, used both inline and in the CTA banner.
    register_label = models.CharField(max_length=60, blank=True)
    register_url = models.URLField(max_length=600, blank=True)

    # Bottom CTA banner copy.
    cta_title = models.CharField(max_length=200, blank=True)
    cta_subtitle = models.CharField(max_length=300, blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["slug", "-year"]
        constraints = [
            models.UniqueConstraint(fields=["slug", "year"], name="unique_program_page_slug_year"),
        ]

    def __str__(self):
        return f"{self.title} ({self.year})"


class ProgramObjective(models.Model):
    """A "highlight" card on a program page — icon + title + short note.
    Used for grids like "Reunion Highlights" (Reconnect, Inspiring Talks,
    Memorable Moments, ...). Can optionally use a photo instead of an icon."""

    ICON_CHOICES = [
        ("users", "Users (group / reconnect)"),
        ("mic", "Mic (talks / speeches)"),
        ("camera", "Camera (photos / moments)"),
        ("award", "Award (recognition)"),
        ("utensils", "Utensils (food / dinner)"),
        ("gift", "Gift (surprises)"),
        ("calendar", "Calendar (schedule)"),
        ("heart", "Heart (community)"),
        ("music", "Music (entertainment)"),
        ("sparkles", "Sparkles (highlight)"),
    ]

    page = models.ForeignKey(ProgramPage, related_name="objectives", on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=300, blank=True)
    icon = models.CharField(max_length=20, choices=ICON_CHOICES, blank=True)
    image_url = models.URLField(max_length=600, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class ProgramStat(models.Model):
    """A small stat tile (e.g. "Members reached" -> "500+") on a program page edition."""

    page = models.ForeignKey(ProgramPage, related_name="stats", on_delete=models.CASCADE)
    label = models.CharField(max_length=100)
    value = models.CharField(max_length=60)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.label}: {self.value}"


class ProgramGalleryImage(models.Model):
    """A photo in a program page edition's gallery."""

    page = models.ForeignKey(ProgramPage, related_name="gallery", on_delete=models.CASCADE)
    image_url = models.URLField(max_length=600)
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.caption or f"Photo #{self.pk}"


class ProgramTestimonial(models.Model):
    """A participant/beneficiary quote on a program page edition."""

    page = models.ForeignKey(ProgramPage, related_name="testimonials", on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=150, blank=True)
    quote = models.TextField()
    photo_url = models.URLField(max_length=600, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.name} — {self.quote[:40]}"
