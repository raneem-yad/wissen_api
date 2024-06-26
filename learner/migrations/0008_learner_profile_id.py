# Generated by Django 4.2 on 2024-05-19 07:55

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("learner", "0007_alter_learner_owner"),
    ]

    operations = [
        migrations.AddField(
            model_name="learner",
            name="profile_id",
            field=models.CharField(
                default=uuid.uuid4, editable=False, max_length=255
            ),
        ),
    ]
