from rest_framework import serializers
from .models import Course, VideoContent


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'course_name', 'summery', 'level', 'description', 'course_requirements', 'learning_goals',
                  'image', 'is_enrolled', 'posted_date', 'updated_date']


class VideoContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoContent
        fields = ['id', 'course', 'title', 'description', 'video', 'duration',
                  'is_completed', 'created_date', 'updated_date']
