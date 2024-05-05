from django.db import models
from django.contrib.auth.models import User
from djrichtextfield.models import RichTextField
from django_resized import ResizedImageField
from cloudinary_storage.storage import VideoMediaCloudinaryStorage
from cloudinary_storage.validators import validate_video

# Choices here
LEVEL = ((0, "Beginner"), (1, "Intermediate"), (2, "Advanced"))


class Course(models.Model):
    """
    Course model which represent Courses
    """
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=300, unique=True, null=False, blank=False)
    summary = models.CharField(max_length=200)
    description = models.CharField(max_length=500, null=False, blank=False)
    course_requirements = RichTextField(max_length=10000, null=False, blank=False)
    learning_goals = RichTextField(max_length=10000, null=False, blank=False)
    level = models.IntegerField(choices=LEVEL, default=0)
    image = ResizedImageField(
        size=[400, None],
        quality=70,
        upload_to="courses/",
        default="courses/logo_qn9rcl",
        # force_format="WEBP,PNG,JPNG",
        null=False,
        blank=False,
    )
    is_enrolled = models.BooleanField(default=False)
    posted_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_date"]

    def __str__(self):
        return str(self.course_name)


class VideoContent(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, name='course_content')
    title = models.CharField(max_length=255)
    description = models.TextField()
    video = models.FileField(upload_to='videos/', blank=True, storage=VideoMediaCloudinaryStorage(),
                              validators=[validate_video])
    duration = models.IntegerField()  # refer to minutes as video duration
    is_completed = models.BooleanField(default=False)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    def __str__(self):
        return f"the video is {self.video} with duration {self.duration}"
