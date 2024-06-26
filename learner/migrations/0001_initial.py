# Generated by Django 4.2 on 2024-05-07 09:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("courses", "0009_course_tags"),
    ]

    operations = [
        migrations.CreateModel(
            name="Learner",
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
                ("full_name", models.CharField(max_length=200)),
                ("bio", models.TextField(blank=True, null=True)),
                (
                    "image",
                    django_resized.forms.ResizedImageField(
                        blank=True,
                        crop=None,
                        force_format=None,
                        keep_meta=True,
                        null=True,
                        quality=70,
                        scale=None,
                        size=[300, None],
                        upload_to="profiles/",
                    ),
                ),
                ("created_date", models.DateField(auto_now_add=True)),
                ("updated_date", models.DateField(auto_now=True)),
                (
                    "enrolled_courses",
                    models.ManyToManyField(
                        related_name="students", to="courses.course"
                    ),
                ),
                (
                    "owner",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"ordering": ["-created_date"],},
        ),
    ]
