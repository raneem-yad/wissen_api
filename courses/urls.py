from django.urls import path
from .views import (
    CourseList,
    CourseDetails,
    CourseByCategoryList,
    CourseByInstructorList,
    TagsByCourseList,
    EnrollStudentAPIView,
    CourseVideoListView,
    CourseVideoDetailView,
    TopThreeCoursesView,
)

urlpatterns = [
    path("", CourseList.as_view(), name="courses"),
    path("<int:pk>/", CourseDetails.as_view(), name="courses_details"),
    path(
        "by_category/<int:category_id>/",
        CourseByCategoryList.as_view(),
        name="course-by-instructor-list",
    ),
    path(
        "by_instructor/<int:instructor_id>/",
        CourseByInstructorList.as_view(),
        name="course-by-instructor-list",
    ),
    path(
        "<int:course_id>/tags/",
        TagsByCourseList.as_view(),
        name="tags-by-course",
    ),
    path(
        "<int:course_id>/enroll/",
        EnrollStudentAPIView.as_view(),
        name="enroll_student",
    ),
    path(
        "<int:course_id>/videos/",
        CourseVideoListView.as_view(),
        name="course_content",
    ),
    path(
        "<int:course_id>/videos/<int:video_id>",
        CourseVideoDetailView.as_view(),
        name="course_content_details",
    ),
    path("top_three", TopThreeCoursesView.as_view(), name="top_three_courses"),
]
