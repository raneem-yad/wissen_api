# Generated by Django 4.2 on 2024-05-02 05:15

from django.db import migrations, models
import django_resized.forms
import djrichtextfield.models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Course",
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
                ("course_name", models.CharField(max_length=300, unique=True)),
                ("summery", models.CharField(max_length=200)),
                ("description", models.CharField(max_length=500)),
                (
                    "course_requirements",
                    djrichtextfield.models.RichTextField(max_length=10000),
                ),
                (
                    "learning_goals",
                    djrichtextfield.models.RichTextField(max_length=10000),
                ),
                (
                    "level",
                    models.IntegerField(
                        choices=[(0, "Beginner"), (1, "Intermediate"), (2, "Advanced")],
                        default=0,
                    ),
                ),
                (
                    "image",
                    django_resized.forms.ResizedImageField(
                        crop=None,
                        force_format=None,
                        keep_meta=True,
                        quality=70,
                        scale=None,
                        size=[400, None],
                        upload_to="courses/",
                    ),
                ),
                ("is_enrolled", models.BooleanField(default=False)),
                ("posted_date", models.DateTimeField(auto_now=True)),
                ("updated_date", models.DateTimeField(auto_now=True)),
            ],
            options={"ordering": ["-updated_date"],},
        ),
    ]