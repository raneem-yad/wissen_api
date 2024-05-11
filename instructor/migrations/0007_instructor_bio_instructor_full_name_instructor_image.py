# Generated by Django 4.2 on 2024-05-10 10:51

from django.db import migrations, models
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        (
            "instructor",
            "0006_remove_instructor_bio_remove_instructor_full_name_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="instructor",
            name="bio",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="instructor",
            name="full_name",
            field=models.CharField(default="test case", max_length=200),
        ),
        migrations.AddField(
            model_name="instructor",
            name="image",
            field=django_resized.forms.ResizedImageField(
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
    ]