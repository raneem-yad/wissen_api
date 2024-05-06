from django.urls import path
from .views import CourseList, CourseDetails, CourseByCategoryList, CourseByInstructorList, TagsByCourseList

urlpatterns = [
    path('', CourseList.as_view(), name='courses'),
    path('<int:pk>/', CourseDetails.as_view(), name='courses_details'),
    path('by_category/<int:category_id>/', CourseByCategoryList.as_view(), name='course-by-instructor-list'),
    path('by_instructor/<int:instructor_id>/', CourseByInstructorList.as_view(),
         name='course-by-instructor-list'),
    path('<int:course_id>/tags/', TagsByCourseList.as_view(), name='tags-by-course'),

]
