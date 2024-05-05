from django.urls import path

from .views import RatingDetail, RatingList

urlpatterns = [
    path('', RatingList.as_view()),
    path('<int:pk>/', RatingDetail.as_view()),
]