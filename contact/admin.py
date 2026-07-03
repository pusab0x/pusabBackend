from django.contrib import admin

from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ["name", "phone", "blood_group", "university", "session", "subject", "is_read", "created_at"]
    list_filter = ["is_read", "created_at", "university", "blood_group"]
    search_fields = ["name", "phone", "email", "father_name", "mother_name", "university", "village", "school", "college", "message"]
