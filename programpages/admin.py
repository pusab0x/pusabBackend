from django.contrib import admin

from .models import (
    ProgramGalleryImage,
    ProgramInfoItem,
    ProgramObjective,
    ProgramPage,
    ProgramStat,
    ProgramTestimonial,
    ProgramWebinar,
)


class ProgramObjectiveInline(admin.TabularInline):
    model = ProgramObjective
    extra = 1


class ProgramInfoItemInline(admin.TabularInline):
    model = ProgramInfoItem
    extra = 1


class ProgramStatInline(admin.TabularInline):
    model = ProgramStat
    extra = 1


class ProgramGalleryImageInline(admin.TabularInline):
    model = ProgramGalleryImage
    extra = 1


class ProgramTestimonialInline(admin.TabularInline):
    model = ProgramTestimonial
    extra = 1


class ProgramWebinarInline(admin.TabularInline):
    model = ProgramWebinar
    extra = 1


@admin.register(ProgramPage)
class ProgramPageAdmin(admin.ModelAdmin):
    list_display = ["slug", "year", "title", "updated_at"]
    list_filter = ["slug", "year"]
    search_fields = ["slug", "title"]
    inlines = [
        ProgramObjectiveInline,
        ProgramInfoItemInline,
        ProgramStatInline,
        ProgramGalleryImageInline,
        ProgramTestimonialInline,
        ProgramWebinarInline,
    ]
