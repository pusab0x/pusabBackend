from django.db import models


class PublicityPost(models.Model):
    """News / press release / event. Optional external `link` opens the source."""

    class Type(models.TextChoices):
        NEWS = "news", "News"
        PRESS = "press", "Press release"
        EVENT = "event", "Event"
        BLOG = "blog", "Column"

    type = models.CharField(max_length=10, choices=Type.choices, default=Type.NEWS)
    title = models.CharField(max_length=300)
    excerpt = models.CharField(max_length=400, blank=True)
    body = models.TextField(blank=True)
    link = models.URLField(max_length=600, blank=True)
    image_url = models.URLField(max_length=600, blank=True)
    date = models.DateField(null=True, blank=True)
    # Byline, shown on columns. Blank for the other post types.
    author = models.CharField(max_length=200, blank=True)
    published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return self.title
