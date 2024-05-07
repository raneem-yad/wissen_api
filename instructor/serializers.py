from rest_framework import serializers

from expertise.serializers import ExpertiseSerializer
from .models import Instructor


class InstructorSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')  # one-to-one relationship
    is_owner = serializers.SerializerMethodField()
    expertise = ExpertiseSerializer(many=True, read_only=True)

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Instructor
        fields = ['id', 'owner','expertise', 'job_title',
                  'website_link', 'linkedin_link', 'is_owner',
                  'created_date', 'updated_date']
