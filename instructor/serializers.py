from django.db.models import Avg, Count
from rest_framework import serializers

from courses.models import Course, Enrollment
from expertise.serializers import ExpertiseSerializer
from instructor_rating.models import InstructorRating
from .models import Instructor


class InstructorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Instructor model.
    """

    owner = serializers.ReadOnlyField(
        source="owner.username"
    )  # one-to-one relationship
    # is_owner = serializers.SerializerMethodField()
    expertise = ExpertiseSerializer(many=True, read_only=True)
    rating_value = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField()
    rating_count = serializers.SerializerMethodField()
    course_count = serializers.SerializerMethodField()
    learner_count = serializers.SerializerMethodField()

    # def get_is_owner(self, obj):
    #     if self.context['request'] :
    #         request = self.context['request']
    #         return request.user == obj.owner

    def get_rating_value(self, obj):
        return InstructorRating.objects.filter(teacher=obj).aggregate(
            avg_rating=Avg("rating")
        )["avg_rating"]

    def get_rating_count(self, obj):
        return InstructorRating.objects.filter(teacher=obj).count()

    def get_course_count(self, obj):
        return Course.objects.filter(teacher=obj.owner).count()

    def get_learner_count(self, obj):
        # Get the courses taught by the instructor
        courses = Course.objects.filter(teacher=obj.owner)
        # Count the total number of unique learners enrolled in these courses
        return (
            Enrollment.objects.filter(course__in=courses)
            .values("user")
            .distinct()
            .count()
        )

    class Meta:
        model = Instructor
        fields = [
            "id",
            "owner",
            "profile_id",
            "expertise",
            "job_title",
            "rating_value",
            "rating_count",
            "course_count",
            "learner_count",
            "image",
            "bio",
            "website_link",
            "linkedin_link",
            "created_date",
            "updated_date",
        ]
