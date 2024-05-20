import uuid
from django.db import models
from django.contrib.auth.models import User
from django_resized import ResizedImageField


class Learner(models.Model):
    """
       A model representing a learner profile associated with a user.

       Fields:
       - owner: A one-to-one relationship with the User model.
       - full_name: The full name of the learner.
       - bio: A brief biography of the learner.
       - profile_id: A unique identifier for the profile, automatically generated if not provided.
       - image: An optional profile image for the learner, resized to 300px wide and 70% quality.
       - created_date: The date and time when the profile was created, set automatically.
       - updated_date: The date and time when the profile was last updated, set automatically.

       Methods:
       - save: Overrides the save method to automatically generate a profile_id if it is not already set.

       Meta:
       - ordering: Orders the learner profiles by creation date in descending order.
       """

    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, null=False, blank=False)
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
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.profile_id:
            self.profile_id = str(uuid.uuid4())
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-created_date"]

    def __str__(self):
        return f"{self.owner}'s learner profile"
