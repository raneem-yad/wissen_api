from django.db import IntegrityError
from rest_framework import serializers

from .models import InstructorRating


class InstructorRatingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = InstructorRating
        fields = ["id", "created_at", "teacher", "user", "rating"]

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                {"detail": "you have already rated this"}
            )
