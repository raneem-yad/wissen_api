from django.contrib.auth.models import User
from django.db.models import Avg
from rest_framework import serializers

from category.models import Category
from comment.models import Comment
from comment.serializers import CommentSerializer
from learner.models import Learner
from rating.models import Rating
from tags.models import Tags
from tags.serializers import TagsSerializer
from .models import Course, VideoContent


class CourseSerializer(serializers.ModelSerializer):
    level_label = serializers.SerializerMethodField()

    teacher = serializers.ReadOnlyField(
        source="teacher.username"
    )  # one-to-one relationship
    is_course_owner = serializers.SerializerMethodField()
    teacher_profile_id = serializers.ReadOnlyField(
        source="teacher.instructor.profile_id"
    )
    teacher_image = serializers.ReadOnlyField(
        source="teacher.instructor.image.url"
    )

    category = serializers.PrimaryKeyRelatedField(
        source="course_category", queryset=Category.objects.all()
    )
    category_name = serializers.ReadOnlyField(
        source="course_category.name"
    )  # one-to-many relationship
    category_id = serializers.ReadOnlyField(source="course_category.id")

    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tags.objects.all()
    )
    # tags_details = serializers.ReadOnlyField(source='get_tags_details')
    tags_details = serializers.StringRelatedField(
        source="tags", many=True, read_only=True
    )

    students = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    students_count = serializers.ReadOnlyField(
        source="students.count", read_only=True
    )
    students_names = serializers.StringRelatedField(many=True, read_only=True)
    student_id = serializers.SerializerMethodField()
    is_learner_enrolled_in_course = serializers.SerializerMethodField()

    rating_value = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()

    comments_count = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    def get_level_label(self, obj):
        return obj.get_level_display()

    def get_is_course_owner(self, obj):
        request = self.context["request"]
        return request.user == obj.teacher

    def get_student_id(self, obj):
        request = self.context["request"]
        if request and request.user.is_authenticated:
            learner = Learner.objects.filter(owner=request.user).first()
            if learner:
                return learner.id
            return None
        return None

    def get_is_learner_enrolled_in_course(self, obj):
        request = self.context["request"]
        if request and request.user.is_authenticated:
            learner = Learner.objects.filter(owner=request.user).first()
            learners = Learner.objects.filter(owner__in=obj.students.all())
            if learner:
                return learner in learners
        return False

    def get_rating_value(self, obj):
        # Calculate average rating for the course
        return (
            Rating.objects.filter(course=obj).aggregate(Avg("rating"))[
                "rating__avg"
            ]
            or 0
        )

    def get_rating_count(self, obj):
        # Count the number of ratings for the course
        return (
            Rating.objects.filter(course=obj).values("user").distinct().count()
        )

    def get_comments_count(self, obj):
        comments_count = (
            Comment.objects.filter(course=obj)
            .values("owner")
            .distinct()
            .count()
        )
        return comments_count

    def get_comments(self, obj):
        comments_qs = Comment.objects.filter(course=obj)
        comments_serializer = CommentSerializer(
            comments_qs, many=True, context=self.context
        )
        return comments_serializer.data

    class Meta:
        model = Course
        fields = [
            "id",
            "course_name",
            "category",
            "category_name",
            "category_id",
            "summery",
            "level",
            "level_label",
            "course_requirements",
            "learning_goals",
            "tags",
            "tags_details",
            "students",
            "students_count",
            "students_names",
            "student_id",
            "description",
            "is_learner_enrolled_in_course",
            "rating_value",
            "rating_count",
            "comments",
            "comments_count",
            "image",
            "teacher",
            "is_course_owner",
            "teacher_profile_id",
            "teacher_image",
            "posted_date",
            "updated_date",
        ]


class VideoContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoContent
        fields = [
            "id",
            "video_contents",
            "title",
            "description",
            "video",
            "duration",
            "is_completed",
            "created_date",
            "updated_date",
        ]
