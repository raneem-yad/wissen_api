from django.urls import path

from .views import ExpertiseList, ExpertiseDetail, InstructorsByExpertiseList

urlpatterns = [
    path("", ExpertiseList.as_view()),
    path("<int:pk>/", ExpertiseDetail.as_view()),
    path(
        "<int:pk>/instructors/",
        InstructorsByExpertiseList.as_view(),
        name="courses-by-tag",
    ),
]
