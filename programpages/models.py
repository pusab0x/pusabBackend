from django.db import models


class ProgramPage(models.Model):
    """Rich content for one program's dedicated page (e.g. Annual Reunion,
    PUSAB Scholarship). Keyed by a slug matching the frontend route
    (/programs/<slug>) and the PROGRAMS entry in site-content.ts."""

    slug = models.SlugField(max_length=60, unique=True)
    title = models.CharField(max_length=200)
    tagline = models.CharField(max_length=300, blank=True)
    hero_image_url = models.URLField(max_length=600, blank=True)
    overview = models.TextField(blank=True)
    eligibility = models.TextField(blank=True)
    process = models.TextField(blank=True)
    schedule_note = models.CharField(max_length=300, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["slug"]

    def __str__(self):
        return self.title


class ProgramObjective(models.Model):
    """A compact photo + short-note card under a program page's "Objectives" section."""

    page = models.ForeignKey(ProgramPage, related_name="objectives", on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=300, blank=True)
    image_url = models.URLField(max_length=600, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class ProgramStat(models.Model):
    """A small stat tile (e.g. "Members reached" -> "500+") on a program page.
    Tagged with a year so recurring, once-a-year programs (like the Annual
    Reunion) can show a different set of stats per edition."""

    page = models.ForeignKey(ProgramPage, related_name="stats", on_delete=models.CASCADE)
    year = models.PositiveIntegerField(null=True, blank=True)
    label = models.CharField(max_length=100)
    value = models.CharField(max_length=60)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-year", "order", "id"]

    def __str__(self):
        return f"{self.label}: {self.value}"


class ProgramGalleryImage(models.Model):
    """A photo in a program page's gallery, tagged with the year it's from."""

    page = models.ForeignKey(ProgramPage, related_name="gallery", on_delete=models.CASCADE)
    year = models.PositiveIntegerField(null=True, blank=True)
    image_url = models.URLField(max_length=600)
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-year", "order", "id"]

    def __str__(self):
        return self.caption or f"Photo #{self.pk}"


class ProgramTestimonial(models.Model):
    """A participant/beneficiary quote on a program page, tagged with the
    year it's from."""

    page = models.ForeignKey(ProgramPage, related_name="testimonials", on_delete=models.CASCADE)
    year = models.PositiveIntegerField(null=True, blank=True)
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=150, blank=True)
    quote = models.TextField()
    photo_url = models.URLField(max_length=600, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-year", "order", "id"]

    def __str__(self):
        return f"{self.name} — {self.quote[:40]}"
