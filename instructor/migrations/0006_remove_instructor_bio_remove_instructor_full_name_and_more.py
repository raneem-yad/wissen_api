# Generated by Django 4.2 on 2024-05-07 16:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("instructor", "0005_instructor_expertise"),
    ]

    operations = [
        migrations.RemoveField(model_name="instructor", name="bio",),
        migrations.RemoveField(model_name="instructor", name="full_name",),
        migrations.RemoveField(model_name="instructor", name="image",),
    ]
