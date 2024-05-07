from django.urls import path
from .views import LearnerList, LearnerDetail

urlpatterns = [
    path('', LearnerList.as_view(), name='learners_list'),
    path('<int:pk>/', LearnerDetail.as_view(), name='learner_details'),
]
