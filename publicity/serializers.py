from rest_framework import serializers

from .models import PublicityPost


class PublicityPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicityPost
        fields = [
            "id",
            "type",
            "title",
            "excerpt",
            "body",
            "link",
            "image_url",
            "date",
            "author",
            "published",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]
