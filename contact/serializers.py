from rest_framework import serializers

from .models import ContactMessage


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = [
            "id", "name", "phone", "father_name", "mother_name", "blood_group", "subject",
            "university", "session", "union_name", "village", "school", "college",
            "message", "email", "is_read", "created_at",
        ]
        read_only_fields = ["id", "created_at"]
