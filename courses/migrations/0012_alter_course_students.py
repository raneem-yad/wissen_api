# Generated by Django 4.2 on 2024-05-13 10:41

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("courses", "0011_remove_course_is_enrolled"),
    ]

    operations = [
        migrations.AlterField(
            model_name="course",
            name="students",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="courses_enrolled",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
