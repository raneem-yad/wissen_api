import uuid
from django.db import models
from django.contrib.auth.models import User
from django_resized import ResizedImageField

from expertise.models import Expertise


class Instructor(models.Model):
    """
    A model representing a instructor profile associated with a user.

    """

    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=100, null=True, blank=True)
    full_name = models.CharField(
        max_length=200, null=False, blank=False, default="test case"
    )
    bio = models.TextField(null=True, blank=True)
    profile_id = models.CharField(
        max_length=255, unique=True, editable=False, default=uuid.uuid4
    )
    image = ResizedImageField(
        size=[300, None],
        quality=70,
        upload_to="profiles/",
        default="profiles/default_profile_iryl59",
        null=True,
        blank=True,
    )
    website_link = models.URLField(null=True, blank=True)
    linkedin_link = models.URLField(null=True, blank=True)
    expertise = models.ManyToManyField(Expertise, related_name="instructors")
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.profile_id:
            self.profile_id = str(uuid.uuid4())
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-created_date"]

    def __str__(self):
        return f"{self.owner}'s instructor profile"
