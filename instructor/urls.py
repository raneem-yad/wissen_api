from django.urls import path
from .views import InstructorList

urlpatterns = [
    path('', InstructorList.as_view(), name='instructors_list')
]
