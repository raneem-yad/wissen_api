# Generated by Django 4.2 on 2024-05-19 08:04

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("instructor", "0009_instructor_profile_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="instructor",
            name="profile_id",
            field=models.CharField(
                default=uuid.uuid4, editable=False, max_length=255, unique=True
            ),
        ),
    ]
