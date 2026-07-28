from django.contrib import admin

from .models import PageHero, PageHeroImage


class PageHeroImageInline(admin.TabularInline):
    model = PageHeroImage
    extra = 1


@admin.register(PageHero)
class PageHeroAdmin(admin.ModelAdmin):
    list_display = ["page", "title", "updated_at"]
    inlines = [PageHeroImageInline]
