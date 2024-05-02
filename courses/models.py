from django.db import models
from djrichtextfield.models import RichTextField
from django_resized import ResizedImageField

# Choices here
LEVEL = ((0, "Beginner"), (1, "Intermediate"), (2, "Advanced"))

class Course(models.Model):
    """
    Course model which represent Courses
    """
    course_name = models.CharField(max_length=300, unique=True, null=False, blank=False)
    summery = models.CharField(max_length=200)
    description = models.CharField(max_length=500, null=False, blank=False)
    course_requirements = RichTextField(max_length=10000, null=False, blank=False)
    learning_goals = RichTextField(max_length=10000, null=False, blank=False)
    level = models.IntegerField(choices=LEVEL, default=0)
    image = ResizedImageField(
        size=[400, None],
        quality=70,
        upload_to="courses/",
        # force_format="WEBP,PNG,JPNG",
        null=False,
        blank=False,
    )
    is_enrolled = models.BooleanField(default=False)
    posted_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_date"]

    def __str__(self):
        return str(self.course_name)