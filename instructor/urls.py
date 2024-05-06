from django.urls import path
from .views import InstructorList, InstructorDetails, ExpertiseByInstructorList

urlpatterns = [
    path('', InstructorList.as_view(), name='instructors_list'),
    path('<int:pk>/', InstructorDetails.as_view(), name='instructors_details'),
    path('<int:pk>/expertise/', ExpertiseByInstructorList.as_view(), name='tags-by-course'),
]
