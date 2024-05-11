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


# class MyCustomRegistrationSerializer(RegisterSerializer):
#     CHOICES = (
#         ('I', 'Instructor'),
#         ('S', 'Student'),
#     )
#     role = serializers.ChoiceField(max_length=1, choices=CHOICES)
#
#     def get_cleaned_data(self):
#         data_dict = super().get_cleaned_data()
#         data_dict['role'] = self.validated_data.get('role', '')
#         return data_dict

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
