# Generated by Django 4.2 on 2024-05-02 13:15

import cloudinary_storage.storage
import cloudinary_storage.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0002_videocontent"),
    ]

    operations = [
        migrations.AlterField(
            model_name="videocontent",
            name="video",
            field=models.FileField(
                blank=True,
                storage=cloudinary_storage.storage.VideoMediaCloudinaryStorage(),
                upload_to="videos/",
                validators=[cloudinary_storage.validators.validate_video],
            ),
        ),
    ]