from django.db import models


class PageHero(models.Model):
    """The hero banner (title + subtitle + one or more images) for a page.

    One row per page, looked up by `page` (e.g. "home", "about", "programs").
    Pages with a single hero photo just have one related PageHeroImage; the
    home page can have several, cycled as a slideshow.
    """

    PAGE_CHOICES = [
        ("home", "Home"),
        ("about", "About"),
        ("programs", "Programs"),
        ("leadership", "Leadership"),
        ("moments", "Moments"),
        ("publicity", "Publicity"),
        ("convening-committee", "Convening Committee"),
        ("honor-board", "Honor Board"),
    ]

    page = models.CharField(max_length=40, choices=PAGE_CHOICES, unique=True)
    title = models.CharField(max_length=200, blank=True)
    lede = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["page"]

    def __str__(self):
        return f"{self.get_page_display()} hero"


class PageHeroImage(models.Model):
    """One image in a PageHero's rotation. Most pages have exactly one."""

    hero = models.ForeignKey(PageHero, on_delete=models.CASCADE, related_name="images")
    image_url = models.URLField(max_length=600)
    alt_text = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.hero.page} image #{self.order}"
