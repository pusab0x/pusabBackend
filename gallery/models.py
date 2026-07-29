from django.db import models


class GalleryItem(models.Model):
    """A photo in the Moments gallery. Image is hosted on Cloudinary (URL)."""

    title = models.CharField(max_length=200, blank=True)
    caption = models.CharField(max_length=400, blank=True)
    # Free-text so admins can create new categories from the dashboard
    # without a code change. "events" remains the default for new photos.
    category = models.CharField(max_length=40, default="events")
    year = models.PositiveIntegerField(null=True, blank=True)
    image_url = models.URLField(max_length=600)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title or f"Photo #{self.pk}"
