# Generated by Django 4.2 on 2024-05-19 08:04

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("instructor", "0008_alter_instructor_job_title"),
    ]

    operations = [
        migrations.AddField(
            model_name="instructor",
            name="profile_id",
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=255),
        ),
    ]