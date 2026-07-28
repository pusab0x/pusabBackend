from rest_framework import serializers

from .models import PageHero, PageHeroImage


class PageHeroImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageHeroImage
        fields = ["id", "image_url", "alt_text", "order"]
        read_only_fields = ["id"]


class PageHeroSerializer(serializers.ModelSerializer):
    images = PageHeroImageSerializer(many=True, required=False)

    class Meta:
        model = PageHero
        fields = ["id", "page", "title", "lede", "images", "updated_at"]
        read_only_fields = ["id", "updated_at"]

    def create(self, validated_data):
        images_data = validated_data.pop("images", [])
        hero = PageHero.objects.create(**validated_data)
        self._sync_images(hero, images_data)
        return hero

    def update(self, instance, validated_data):
        images_data = validated_data.pop("images", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if images_data is not None:
            self._sync_images(instance, images_data)
        return instance

    @staticmethod
    def _sync_images(hero, images_data):
        # Replace the whole set on every write — simpler than diffing, and the
        # dashboard always sends the full ordered list.
        hero.images.all().delete()
        PageHeroImage.objects.bulk_create(
            [
                PageHeroImage(
                    hero=hero,
                    image_url=img.get("image_url", ""),
                    alt_text=img.get("alt_text", ""),
                    order=img.get("order", i),
                )
                for i, img in enumerate(images_data)
            ]
        )
