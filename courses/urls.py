from django.urls import path
from .views import CourseList, CourseDetails, CourseByCategoryList, CourseByInstructorList

urlpatterns = [
    path('', CourseList.as_view(), name='courses'),
    path('<int:pk>/', CourseDetails.as_view(), name='courses_details'),
    path('courses/by_category/<int:category_id>/', CourseByCategoryList.as_view(), name='course-by-instructor-list'),
    path('courses/by_instructor/<int:instructor_id>/', CourseByInstructorList.as_view(),
         name='course-by-instructor-list'),

]
