from rest_framework import serializers
from .models import Instructor


class InstructorSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')  # one-to-one relationship

    class Meta:
        model = Instructor
        fields = ['id', 'owner', 'full_name', 'bio', 'job_title', 'website_link', 'linkedin_link',
                  'image', 'created_date', 'updated_date']
