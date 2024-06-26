# Generated by Django 4.2 on 2024-05-03 11:00

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        (
            "instructor",
            "0002_alter_instructor_bio_alter_instructor_image_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="instructor",
            name="image",
            field=django_resized.forms.ResizedImageField(
                blank=True,
                crop=None,
                default="../courses/logo_qn9rcl",
                force_format=None,
                keep_meta=True,
                null=True,
                quality=70,
                scale=None,
                size=[300, None],
                upload_to="profiles/",
            ),
        ),
    ]
