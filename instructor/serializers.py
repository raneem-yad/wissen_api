from django.db.models import Avg, Count
from rest_framework import serializers

from expertise.serializers import ExpertiseSerializer
from instructor_rating.models import InstructorRating
from .models import Instructor


class InstructorSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')  # one-to-one relationship
    is_owner = serializers.SerializerMethodField()
    expertise = ExpertiseSerializer(many=True, read_only=True)
    rating_value = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_rating_value(self, obj):
        return InstructorRating.objects.filter(teacher=obj).aggregate(avg_rating=Avg('rating'))['avg_rating']

    def get_rating_count(self, obj):
        return InstructorRating.objects.filter(teacher=obj).count()

    class Meta:
        model = Instructor
        fields = ['id', 'owner', 'expertise', 'job_title',
                  'rating_value', 'rating_count',
                  'website_link', 'linkedin_link', 'is_owner',
                  'created_date', 'updated_date']
