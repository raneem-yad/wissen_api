from django.urls import path

from .views import TagsList, TagsDetail, CoursesByTagList

urlpatterns = [
    path("", TagsList.as_view()),
    path("<int:pk>/", TagsDetail.as_view()),
    path(
        "<int:pk>/courses/", CoursesByTagList.as_view(), name="courses-by-tag"
    ),
]
