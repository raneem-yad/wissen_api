from django.contrib.humanize.templatetags.humanize import naturaltime
from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model
    Adds three extra fields when returning a list of Comment instances
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_created_at(self, obj):
        return naturaltime(obj.created_at)

    def get_updated_at(self, obj):
        return naturaltime(obj.updated_at)

    def get_profile_image(self,obj):
        if hasattr(obj.owner, 'learner') and obj.owner.learner.image:
            return str(obj.owner.learner.image.url)
        elif hasattr(obj.owner, 'instructor') and obj.owner.instructor.image:
            return str(obj.owner.instructor.image.url)
        else:
            return None

    def get_profile_id(self, obj):
        if hasattr(obj.owner, 'learner'):
            return obj.owner.learner.id
        elif hasattr(obj.owner, 'instructor'):
            return obj.owner.instructor.id
        else:
            return None

    class Meta:
        model = Comment
        fields = [
            'id', 'owner','profile_id', 'profile_image', 'is_owner', 'created_at', 'updated_at',
            'course', 'created_at', 'updated_at', 'content'
        ]


class CommentDetailSerializer(CommentSerializer):
    """
    Serializer for the Comment model used in Detail view
    Course is a read only field so that we don't have to set it on each update
    """
    course = serializers.ReadOnlyField(source='course.id')