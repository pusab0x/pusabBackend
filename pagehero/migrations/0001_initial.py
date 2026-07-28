# Generated for the pagehero app.

from django.db import migrations, models
import django.db.models.deletion


SEED = [
    {
        "page": "home",
        "title": "Building a stronger future for Bishwambarpur.",
        "lede": "PUSAB brings together students from public universities, medical and engineering colleges to support learning, leadership, and community development in Bishwambarpur.",
    },
    {
        "page": "about",
        "title": "About PUSAB",
        "lede": "Public University Students' Association of Bishwambarpur is a non-political, non-profit student body representing students from public universities, medical and engineering colleges.",
    },
    {
        "page": "programs",
        "title": "Programs & Activities",
        "lede": "From annual reunions to scholarships, medical camps to humanitarian response — here's what PUSAB has delivered, what's running now, and what's next.",
    },
    {
        "page": "leadership",
        "title": "Executive Committee",
        "lede": "The current committee leading PUSAB this session — elected to serve, committed to the community.",
    },
    {
        "page": "moments",
        "title": "Proud Moments",
        "lede": "A photo journey through PUSAB's events, achievements, community service and reunions.",
    },
    {
        "page": "publicity",
        "title": "Publicity",
        "lede": "News, press releases and upcoming events — straight from PUSAB. Tap any story to read the full coverage.",
    },
    {
        "page": "convening-committee",
        "title": "Convening Committee",
        "lede": "The founding committee that established PUSAB on 30 July 2014 — the pioneers who started it all.",
    },
    {
        "page": "honor-board",
        "title": "Honor Board",
        "lede": "With gratitude to those who led PUSAB — the names that shaped the journey, session by session.",
    },
]


def seed_heroes(apps, schema_editor):
    PageHero = apps.get_model("pagehero", "PageHero")
    for row in SEED:
        PageHero.objects.get_or_create(
            page=row["page"],
            defaults={"title": row["title"], "lede": row["lede"]},
        )


def unseed_heroes(apps, schema_editor):
    PageHero = apps.get_model("pagehero", "PageHero")
    PageHero.objects.filter(page__in=[row["page"] for row in SEED]).delete()


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="PageHero",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "page",
                    models.CharField(
                        choices=[
                            ("home", "Home"),
                            ("about", "About"),
                            ("programs", "Programs"),
                            ("leadership", "Leadership"),
                            ("moments", "Moments"),
                            ("publicity", "Publicity"),
                            ("convening-committee", "Convening Committee"),
                            ("honor-board", "Honor Board"),
                        ],
                        max_length=40,
                        unique=True,
                    ),
                ),
                ("title", models.CharField(blank=True, max_length=200)),
                ("lede", models.TextField(blank=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["page"],
            },
        ),
        migrations.CreateModel(
            name="PageHeroImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image_url", models.URLField(max_length=600)),
                ("alt_text", models.CharField(blank=True, max_length=200)),
                ("order", models.PositiveIntegerField(default=0)),
                (
                    "hero",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="pagehero.pagehero",
                    ),
                ),
            ],
            options={
                "ordering": ["order", "id"],
            },
        ),
        migrations.RunPython(seed_heroes, unseed_heroes),
    ]
