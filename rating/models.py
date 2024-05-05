from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg

from courses.models import Course


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rater")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="ratings")
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course} - {self.user}: {self.rating} stars"


    class Meta:
        ordering = ['-created_at']
        unique_together = ("course", "user")

    @classmethod
    def get_average_rating(cls, recipe_id):
        average_rating = cls.objects.filter(recipe_id=recipe_id).aggregate(
            Avg("rating")
        )["rating__avg"]
        return average_rating or 0