from rest_framework import serializers

from tags.serializers import TagsSerializer
from .models import Course, VideoContent


class CourseSerializer(serializers.ModelSerializer):
    teacher = serializers.ReadOnlyField(source='teacher.username')  # one-to-one relationship
    is_course_owner = serializers.SerializerMethodField()
    teacher_id = serializers.ReadOnlyField(source='teacher.instructor.id')
    teacher_image = serializers.ReadOnlyField(source='teacher.instructor.image.url')
    category = serializers.ReadOnlyField(source='course_category.name') # one-to-many relationship
    category_id = serializers.ReadOnlyField(source='course_category.id')
    tags = TagsSerializer(many=True, read_only=True) # many-to-many relationship

    def get_is_course_owner(self, obj):
        request = self.context['request']
        return request.user == obj.teacher

    class Meta:
        model = Course
        fields = ['id', 'course_name', 'category', 'category_id', 'summery', 'level', 'description',
                  'course_requirements', 'learning_goals', 'tags',
                  'image', 'is_enrolled', 'teacher', 'is_course_owner', 'teacher_id', 'teacher_image', 'posted_date',
                  'updated_date']


class VideoContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoContent
        fields = ['id', 'course', 'title', 'description', 'video', 'duration',
                  'is_completed', 'created_date', 'updated_date']
