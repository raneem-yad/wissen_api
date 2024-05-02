from rest_framework import serializers
from .models import Course , LEVEL


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'course_name', 'summery','level', 'description', 'course_requirements', 'learning_goals', 'image',
                  'is_enrolled', 'posted_date', 'updated_date']
