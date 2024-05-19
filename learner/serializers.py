from rest_framework import serializers

from courses.serializers import CourseSerializer
from .models import Learner


class LearnerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Learner model.

    Fields:
    - id: The unique identifier for the learner.
    - owner: The user who owns the learner profile.
    - full_name: The full name of the learner.
    - bio: A brief biography of the learner.
    - image: The profile image of the learner.
    - profile_id: A unique identifier for the profile, read-only.
    - created_date: The date when the profile was created.
    - updated_date: The date when the profile was last updated.
    - enrolled_courses_count: The number of courses the learner is enrolled in.
    - enrolled_courses: A list of courses the learner is enrolled in.

    Methods:
    - get_enrolled_courses: Retrieves and serializes the courses the learner is enrolled in.
    - get_enrolled_courses_count: Retrieves the count of courses the learner is enrolled in.
    """
    enrolled_courses = serializers.SerializerMethodField()
    enrolled_courses_count = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField()

    def get_enrolled_courses(self, obj):
        enrolled_courses = obj.owner.courses_enrolled.all()
        serializer = CourseSerializer(enrolled_courses, many=True, context=self.context)
        return serializer.data

    def get_enrolled_courses_count(self, obj):
        enrolled_courses = obj.owner.courses_enrolled.count()
        return enrolled_courses

    class Meta:
        model = Learner
        fields = ['id', 'owner', 'full_name', 'bio', 'image','profile_id', 'created_date', 'updated_date', 'enrolled_courses_count',
                  'enrolled_courses']
