from rest_framework import serializers
from .models import Learner


class LearnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Learner
        fields = ['id', 'owner', 'full_name', 'bio', 'image', 'created_date', 'updated_date']
