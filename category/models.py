from django.db import models


class Category(models.Model):
    """
    Category Model
    """

    name = models.CharField(
        max_length=100, unique=True, null=False, blank=False
    )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_date"]

    def __str__(self):
        return str(self.name)
