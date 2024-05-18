from django.urls import path

from comment.views import CommentList, CommentDetail

urlpatterns = [
    path('', CommentList.as_view()),
    path('<int:pk>/', CommentDetail.as_view())

]