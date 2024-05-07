from django.db import models
from django.contrib.auth.models import User
from django_resized import ResizedImageField

from courses.models import Course


class Learner(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, null=False, blank=False)
    bio = models.TextField(null=True, blank=True)
    enrolled_courses = models.ManyToManyField(Course, related_name='students')
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
        return f"{self.owner}'s learner profile"
