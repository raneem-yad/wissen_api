# Generated by Django 4.2 on 2024-05-06 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("expertise", "0001_initial"),
        ("instructor", "0004_alter_instructor_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="instructor",
            name="expertise",
            field=models.ManyToManyField(
                related_name="instructors", to="expertise.expertise"
            ),
        ),
    ]