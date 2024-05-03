from django.urls import path
from .views import InstructorList, InstructorDetails

urlpatterns = [
    path('', InstructorList.as_view(), name='instructors_list'),
    path('<int:pk>/', InstructorDetails.as_view(), name='instructors_list'),
]
