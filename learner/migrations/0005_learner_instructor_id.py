# Generated by Django 4.2 on 2024-05-07 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("learner", "0004_alter_learner_owner"),
    ]

    operations = [
        migrations.AddField(
            model_name="learner",
            name="instructor_id",
            field=models.IntegerField(null=True),
        ),
    ]
