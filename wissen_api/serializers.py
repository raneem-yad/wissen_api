from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers

from instructor.models import Instructor
from learner.models import Learner


class CurrentUserSerializer(UserDetailsSerializer):
    profile_id = serializers.ReadOnlyField(source='learner.id')
    profile_image = serializers.ReadOnlyField(source='learner.image.url')

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + (
            'profile_id', 'profile_image'
        )


class CustomRegisterSerializer(RegisterSerializer):
    is_instructor = serializers.BooleanField()

    def custom_signup(self, request, user):
        is_instructor = self.validated_data.get('is_instructor', False)

        if is_instructor:
            Instructor.objects.create(owner=user)
        else:
            Learner.objects.create(owner=user)