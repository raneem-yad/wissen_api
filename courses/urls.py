from django.urls import path
from .views import CourseList, CourseDetails

urlpatterns = [
    path('', CourseList.as_view(), name='courses'),
    path('<int:pk>/', CourseDetails.as_view(), name='courses_details'),
]
