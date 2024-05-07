from django.contrib.auth.models import User
from django.db.models import Avg
from rest_framework import serializers

from learner.models import Learner
from rating.models import Rating
from tags.serializers import TagsSerializer
from .models import Course, VideoContent


class CourseSerializer(serializers.ModelSerializer):
    teacher = serializers.ReadOnlyField(source='teacher.username')  # one-to-one relationship
    is_course_owner = serializers.SerializerMethodField()
    teacher_id = serializers.ReadOnlyField(source='teacher.instructor.id')
    teacher_image = serializers.ReadOnlyField(source='teacher.instructor.image.url')
    category = serializers.ReadOnlyField(source='course_category.name')  # one-to-many relationship
    category_id = serializers.ReadOnlyField(source='course_category.id')
    tags = TagsSerializer(many=True, read_only=True)  # many-to-many relationship
    students = serializers.PrimaryKeyRelatedField(many=True,  queryset=User.objects.all())
    students_names = serializers.StringRelatedField(many=True, read_only=True)
    student_id = serializers.SerializerMethodField()
    is_learner_enrolled_in_course = serializers.SerializerMethodField()
    rating_value = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()

    def get_is_course_owner(self, obj):
        request = self.context['request']
        return request.user == obj.teacher

    def get_student_id(self, obj):
        request = self.context['request']

        learner = Learner.objects.filter(owner=request.user).first()

        if learner:
            return learner.id
        return None

    def get_is_learner_enrolled_in_course(self, obj):
        request = self.context['request']
        if request and request.user.is_authenticated:
            learner = Learner.objects.filter(owner=request.user).first()
            learners = Learner.objects.filter(owner__in=obj.students.all())
            if learner:
                return learner in learners
        return False

    def get_rating_value(self, obj):
        # Calculate average rating for the course
        return Rating.objects.filter(course=obj).aggregate(Avg("rating"))["rating__avg"] or 0

    def get_rating_count(self, obj):
        # Count the number of ratings for the course
        return Rating.objects.filter(course=obj).count()


    class Meta:
        model = Course
        fields = ['id', 'course_name', 'category', 'category_id', 'summery', 'level', 'description',
                  'course_requirements', 'learning_goals', 'tags', 'students', 'students_names', 'student_id',
                  'is_learner_enrolled_in_course', 'rating_value', 'rating_count',
                  'image', 'teacher', 'is_course_owner', 'teacher_id', 'teacher_image', 'posted_date',
                  'updated_date']


class VideoContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoContent
        fields = ['id', 'course', 'title', 'description', 'video', 'duration',
                  'is_completed', 'created_date', 'updated_date']