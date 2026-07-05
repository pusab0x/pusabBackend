"""Turn ProgramPage into one row per (slug, year) edition.

Existing rows (which predate per-year editions) are backfilled with the
current year so they keep working as "this year's" edition. Stat,
GalleryImage and Testimonial had a per-item `year` field from an earlier
migration that's now redundant — the parent page IS the year — so it's
removed here.
"""
from datetime import date

from django.db import migrations, models


BACKFILL_YEAR = date.today().year


def backfill_year(apps, schema_editor):
    ProgramPage = apps.get_model("programpages", "ProgramPage")
    ProgramPage.objects.filter(year__isnull=True).update(year=BACKFILL_YEAR)


class Migration(migrations.Migration):

    dependencies = [
        ("programpages", "0003_alter_programgalleryimage_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="programpage",
            name="year",
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.RunPython(backfill_year, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="programpage",
            name="year",
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name="programpage",
            name="slug",
            field=models.SlugField(max_length=60),
        ),
        migrations.AlterModelOptions(
            name="programpage",
            options={"ordering": ["slug", "-year"]},
        ),
        migrations.AddConstraint(
            model_name="programpage",
            constraint=models.UniqueConstraint(fields=("slug", "year"), name="unique_program_page_slug_year"),
        ),
        migrations.RemoveField(
            model_name="programstat",
            name="year",
        ),
        migrations.RemoveField(
            model_name="programgalleryimage",
            name="year",
        ),
        migrations.RemoveField(
            model_name="programtestimonial",
            name="year",
        ),
        migrations.AlterModelOptions(
            name="programstat",
            options={"ordering": ["order", "id"]},
        ),
        migrations.AlterModelOptions(
            name="programgalleryimage",
            options={"ordering": ["order", "id"]},
        ),
        migrations.AlterModelOptions(
            name="programtestimonial",
            options={"ordering": ["order", "id"]},
        ),
    ]
