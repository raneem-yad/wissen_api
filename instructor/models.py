from django.db import models
from django.contrib.auth.models import User
from django_resized import ResizedImageField

from expertise.models import Expertise


class Instructor(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, null=False, blank=False)
    bio = models.TextField(null=True, blank=True)
    job_title = models.CharField(max_length=100)
    website_link = models.URLField(null=True, blank=True)
    linkedin_link = models.URLField(null=True, blank=True)
    expertise = models.ManyToManyField(Expertise, related_name='instructors')
    image = ResizedImageField(
        size=[300, None],
        quality=70,
        upload_to="profiles/",
        null=True, blank=True
    )
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return f"{self.owner}'s instructor profile"
