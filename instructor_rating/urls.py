from django.urls import path

from .views import InstructorRatingList, InstructorRatingDetail

urlpatterns = [
    path("", InstructorRatingList.as_view()),
    path("<int:pk>/", InstructorRatingDetail.as_view()),
]
