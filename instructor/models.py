from django.db import models
from django.contrib.auth.models import User
from django_resized import ResizedImageField


class Instructor(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, name="course_owner")
    name = models.CharField(max_length=200,null=False, blank=False )
    bio = models.TextField(blank=True)
    job_title = models.CharField(max_length=100)
    website_link = models.URLField()
    linkedin_link = models.URLField()
    image = ResizedImageField(
        size=[300, None],
        quality=70,
        upload_to="profiles/",
    )
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)


    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return f"{self.owner}'s instructor profile"