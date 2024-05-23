from django.db import IntegrityError
from rest_framework import serializers

from rating.models import Rating


class RatingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Rating model
    The create method handles the unique constraint on 'user' and 'Course'
    """

    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Rating
        fields = ["id", "created_at", "course", "user", "rating"]

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                {"detail": "you have already rated this course"}
            )
