from rest_framework import serializers
from .models import Course


class CourseSerializer(serializers.ModelSerializer):
    level = serializers.ChoiceField(choices=Course.LEVEL)
    class Meta:
        model = Course
        fields = ['id', 'course_name', 'summery', 'description', 'course_requirements', 'learning_goals', 'image',
                  'is_enrolled', 'posted_date', 'updated_date']
