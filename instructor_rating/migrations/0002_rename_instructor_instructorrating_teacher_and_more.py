# Generated by Django 4.2 on 2024-05-07 08:35

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("instructor", "0005_instructor_expertise"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("instructor_rating", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="instructorrating",
            old_name="instructor",
            new_name="teacher",
        ),
        migrations.AlterUniqueTogether(
            name="instructorrating", unique_together={("teacher", "user")},
        ),
    ]
