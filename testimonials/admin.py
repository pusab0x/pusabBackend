from django.contrib import admin

from .models import Testimonial


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ["name", "role", "is_featured", "order", "created_at"]
    list_filter = ["is_featured"]
    search_fields = ["name", "role", "quote"]
