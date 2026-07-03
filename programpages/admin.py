from django.contrib import admin

from .models import (
    ProgramGalleryImage,
    ProgramObjective,
    ProgramPage,
    ProgramStat,
    ProgramTestimonial,
)


class ProgramObjectiveInline(admin.TabularInline):
    model = ProgramObjective
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


@admin.register(ProgramPage)
class ProgramPageAdmin(admin.ModelAdmin):
    list_display = ["slug", "title", "updated_at"]
    search_fields = ["slug", "title"]
    inlines = [ProgramObjectiveInline, ProgramStatInline, ProgramGalleryImageInline, ProgramTestimonialInline]
