from django.db import migrations

CENTERS = [
    ("বিশ্বম্ভরপুর বালিকা উচ্চ বিদ্যালয়", "বিশ্বম্ভরপুর", "বালিকা উচ্চ বি.", 1),
    ("হাজী মজিদ উল্লাহ পাবলিক উচ্চ বিদ্যালয়", "ফতেপুর", "হাজী মজিদ উল্লাহ", 2),
]


def seed(apps, schema_editor):
    ExamCenter = apps.get_model("exam", "ExamCenter")
    ExamConfig = apps.get_model("exam", "ExamConfig")
    if not ExamCenter.objects.exists():
        for name, location, short, order in CENTERS:
            ExamCenter.objects.create(name=name, location=location, short_name=short, order=order)
    ExamConfig.objects.get_or_create(pk=1)


class Migration(migrations.Migration):
    dependencies = [("exam", "0001_initial")]

    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]
