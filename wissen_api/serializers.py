from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers

from instructor.models import Instructor
from learner.models import Learner


class CustomUserDetailsSerializer(UserDetailsSerializer):
    profile_image = serializers.SerializerMethodField()
    profile_id = serializers.SerializerMethodField()
    profile_type = serializers.SerializerMethodField()

    def get_profile_image(self, user):
        if hasattr(user, 'learner') and user.learner.image:
            return str(user.learner.image.url)
        elif hasattr(user, 'instructor') and user.instructor.image:
            return str(user.instructor.image.url)
        else:
            return None

    def get_profile_id(self, user):
        if hasattr(user, 'learner'):
            return user.learner.id
        elif hasattr(user, 'instructor'):
            return user.instructor.id
        else:
            return None

    def get_profile_type(self, user):
        if hasattr(user, 'learner'):
            return 'learner'
        elif hasattr(user, 'instructor'):
            return 'instructor'
        else:
            return None

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + (
            'profile_id', 'profile_image', 'profile_type'
        )

class CustomRegisterSerializer(RegisterSerializer):
    is_instructor = serializers.BooleanField()
    full_name = serializers.CharField()

    def validate(self, attrs):
        # Call the parent's validate method first
        attrs = super().validate(attrs)

        # Check if 'is_instructor' is provided and is a boolean
        if 'is_instructor' not in attrs:
            raise serializers.ValidationError("is_instructor field is required.")
        if not isinstance(attrs['is_instructor'], bool):
            raise serializers.ValidationError("is_instructor must be a boolean.")

        # Check if 'full_name' is provided and not empty
        if 'full_name' not in attrs or not attrs['full_name'].strip():
            raise serializers.ValidationError("full_name field is required.")

        return attrs

    def custom_signup(self, request, user):
        print("custom_signup method called.")
        is_instructor = self.validated_data.get('is_instructor', False)
        full_name = self.validated_data.get('full_name', "Not found")
        print(f"is_instructor: {is_instructor}, full_name: {full_name}")

        if is_instructor:
            Instructor.objects.create(owner=user, full_name=full_name)
            print("Instructor profile created.")
        else:
            Learner.objects.create(owner=user, full_name=full_name)
            print("Learner profile created.")
