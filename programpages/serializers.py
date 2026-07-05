from rest_framework import serializers

from .models import (
    ProgramGalleryImage,
    ProgramObjective,
    ProgramPage,
    ProgramStat,
    ProgramTestimonial,
)


class ProgramObjectiveSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = ProgramObjective
        fields = ["id", "title", "description", "image_url", "order"]


class ProgramStatSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = ProgramStat
        fields = ["id", "label", "value", "order"]


class ProgramGalleryImageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = ProgramGalleryImage
        fields = ["id", "image_url", "caption", "order"]


class ProgramTestimonialSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = ProgramTestimonial
        fields = ["id", "name", "role", "quote", "photo_url", "order"]


class ProgramPageSerializer(serializers.ModelSerializer):
    """Reads/writes one (slug, year) edition of a program page plus all its
    nested content in one shot. Nested lists are fully replaced on write —
    the dashboard always sends the complete list for each section, so a
    simple delete-and-recreate keeps this predictable without diffing ids."""

    objectives = ProgramObjectiveSerializer(many=True, required=False)
    stats = ProgramStatSerializer(many=True, required=False)
    gallery = ProgramGalleryImageSerializer(many=True, required=False)
    testimonials = ProgramTestimonialSerializer(many=True, required=False)

    class Meta:
        model = ProgramPage
        fields = [
            "id", "slug", "year", "title", "tagline", "hero_image_url",
            "overview", "eligibility", "process", "schedule_note",
            "objectives", "stats", "gallery", "testimonials",
            "updated_at",
        ]
        read_only_fields = ["id", "updated_at"]

    def create(self, validated_data):
        nested = self._pop_nested(validated_data)
        page = ProgramPage.objects.create(**validated_data)
        self._save_nested(page, nested)
        return page

    def update(self, instance, validated_data):
        nested = self._pop_nested(validated_data)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        self._save_nested(instance, nested, replace=True)
        return instance

    @staticmethod
    def _pop_nested(validated_data):
        return {
            "objectives": validated_data.pop("objectives", None),
            "stats": validated_data.pop("stats", None),
            "gallery": validated_data.pop("gallery", None),
            "testimonials": validated_data.pop("testimonials", None),
        }

    @staticmethod
    def _save_nested(page, nested, replace=False):
        model_map = {
            "objectives": ProgramObjective,
            "stats": ProgramStat,
            "gallery": ProgramGalleryImage,
            "testimonials": ProgramTestimonial,
        }
        for key, model in model_map.items():
            rows = nested.get(key)
            if rows is None:
                continue
            if replace:
                model.objects.filter(page=page).delete()
            for row in rows:
                row.pop("id", None)
                model.objects.create(page=page, **row)
