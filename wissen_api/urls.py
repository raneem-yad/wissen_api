"""
URL configuration for wissen_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from wissen_api.views import logout_route

schema_view = get_schema_view(
    openapi.Info(
        title="Wissen Website API",
        default_version='v1',
        description="My Wissen Website API description",
        contact=openapi.Contact(email="ranoprog@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path("api-auth/", include('rest_framework.urls')),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    # our logout route has to be above the default one to be matched first
    path('dj-rest-auth/logout/', logout_route),
    path(
        'dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')
    ),
    path("djrichtextfield/", include("djrichtextfield.urls")),

    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path("courses/", include('courses.urls')),
    path("instructors/", include('instructor.urls')),
    path("categories/", include('category.urls')),
    path("comments/", include('comment.urls')),
    path("rating/", include('rating.urls')),
    path("tags/", include('tags.urls')),
    path("expertise/", include('expertise.urls')),
    path("instructor-rating/", include('instructor_rating.urls')),
    path("learners/", include('learner.urls')),

]
