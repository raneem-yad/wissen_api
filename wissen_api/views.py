from dj_rest_auth.registration.views import RegisterView
from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status

from instructor.models import Instructor
from learner.models import Learner
from .serializers import CustomRegisterSerializer, CustomUserDetailsSerializer, ProfileSerializer
from .settings import (
    JWT_AUTH_COOKIE, JWT_AUTH_REFRESH_COOKIE, JWT_AUTH_SAMESITE,
    JWT_AUTH_SECURE,
)


# dj-rest-auth logout view fix
@api_view(['POST'])
def logout_route(request):
    """
    Addresses an issue with:
    dj-rest-auth has a bug that doesn't allow users to log out.
    we set both cookies to an empty string and pass additional
    attributes like secure, httponly and samesite, which was
    left out by mistake by the library.
    """
    response = Response()
    response.set_cookie(
        key=JWT_AUTH_COOKIE,
        value='',
        httponly=True,
        expires='Thu, 01 Jan 1970 00:00:00 GMT',
        max_age=0,
        samesite=JWT_AUTH_SAMESITE,
        secure=JWT_AUTH_SECURE,
    )
    response.set_cookie(
        key=JWT_AUTH_REFRESH_COOKIE,
        value='',
        httponly=True,
        expires='Thu, 01 Jan 1970 00:00:00 GMT',
        max_age=0,
        samesite=JWT_AUTH_SAMESITE,
        secure=JWT_AUTH_SECURE,
    )
    return response


class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer


class ProfileRetrieveAPIView(RetrieveAPIView):
    lookup_field = 'profile_id'

    def get(self, request, *args, **kwargs):
        profile_id = kwargs.get('profile_id')
        try:
            learner = Learner.objects.get(profile_id=profile_id)
            profile_data = {
                'role': 'learner',
                'profile': learner
            }
            serializer = ProfileSerializer(profile_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Learner.DoesNotExist:
            pass

        try:
            instructor = Instructor.objects.get(profile_id=profile_id)
            profile_data = {
                'role': 'instructor',
                'profile': instructor
            }
            serializer = ProfileSerializer(profile_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Instructor.DoesNotExist:
            pass

        # Profile not found
        return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
