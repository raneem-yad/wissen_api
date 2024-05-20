from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg

from instructor.models import Instructor


class InstructorRating(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="instructor_rater"
    )
    teacher = models.ForeignKey(
        Instructor, on_delete=models.CASCADE, related_name="instructor_ratings"
    )
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.teacher} - {self.user}: {self.rating} stars"

    class Meta:
        ordering = ["-created_at"]
        unique_together = ("teacher", "user")

    @classmethod
    def get_average_rating(cls, instructor_id):
        average_rating = cls.objects.filter(
            instructor_id=instructor_id
        ).aggregate(Avg("rating"))["rating__avg"]
        return average_rating or 0
