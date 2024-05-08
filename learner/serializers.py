from rest_framework import serializers

from courses.serializers import CourseSerializer
from .models import Learner


class LearnerSerializer(serializers.ModelSerializer):
    enrolled_courses = serializers.SerializerMethodField()
    enrolled_courses_count = serializers.SerializerMethodField()
    # courses_enrolled = CourseSerializer(many=True, read_only=True)

    def get_enrolled_courses(self, obj):
        enrolled_courses = obj.owner.courses_enrolled.all()
        serializer = CourseSerializer(enrolled_courses, many=True, context=self.context)
        return serializer.data

    def get_enrolled_courses_count(self, obj):
        enrolled_courses = obj.owner.courses_enrolled.count()
        return enrolled_courses


    class Meta:
        model = Learner
        fields = ['id', 'owner', 'full_name', 'bio', 'image', 'created_date', 'updated_date','enrolled_courses_count','enrolled_courses']
