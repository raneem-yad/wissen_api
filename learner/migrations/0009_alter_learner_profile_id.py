# Generated by Django 4.2 on 2024-05-19 07:59

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("learner", "0008_learner_profile_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="learner",
            name="profile_id",
            field=models.CharField(
                default=uuid.uuid4, editable=False, max_length=255, unique=True
            ),
        ),
    ]