from dj_rest_auth.registration.views import RegisterView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import CustomRegisterSerializer
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

    # def perform_create(self, serializer):
    #     user = serializer.save(self.request)
    #     serializer.custom_signup(self.request, user)
