# Generated by Django 4.2 on 2024-05-16 20:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0014_enrollment"),
    ]

    operations = [
        migrations.DeleteModel(name="Enrollment",),
    ]