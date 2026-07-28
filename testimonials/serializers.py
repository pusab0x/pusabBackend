from rest_framework import serializers

from .models import Testimonial


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ["id", "name", "role", "quote", "photo_url", "program", "is_featured", "order", "created_at"]
        read_only_fields = ["id", "created_at"]
