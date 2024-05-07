from django.contrib.auth.models import User
from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from category.models import Category
from instructor.models import Instructor
from learner.models import Learner
from tags.models import Tags
from tags.serializers import TagsSerializer
from wissen_api.permissions import HasInstructorProfile, IsInstructorOrReadOnly
from .models import Course
from .serializers import CourseSerializer


class CourseList(APIView):
    serializer_class = CourseSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]

    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(
            courses, many=True, context={'request': request}
        )
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CourseSerializer)
    def post(self, request):
        # Allow only instructors to create a course
        if not HasInstructorProfile().has_permission(request, self):
            return Response(
                {"detail": "You must have an instructor profile to create a course."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = CourseSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save(teacher=request.user)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class CourseDetails(APIView):
    serializer_class = CourseSerializer
    permission_classes = [IsInstructorOrReadOnly]

    def get_object(self, pk):
        try:
            course = Course.objects.get(pk=pk)
            self.check_object_permissions(self.request, course)
            return course
        except Course.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        course = self.get_object(pk)

        serializer = CourseSerializer(course, context={'request': request})
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CourseSerializer)
    def put(self, request, pk):
        # Allow only instructors to update a course
        if not HasInstructorProfile().has_permission(request, self):
            return Response(
                {"detail": "You must have an instructor profile to create a course."},
                status=status.HTTP_403_FORBIDDEN
            )
        course = self.get_object(pk)
        serializer = CourseSerializer(course, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # Allow only instructors to delete a course
        if not HasInstructorProfile().has_permission(request, self):
            return Response(
                {"detail": "You must have an instructor profile to create a course."},
                status=status.HTTP_403_FORBIDDEN
            )
        course = self.get_object(pk)
        course.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


class EnrollStudentAPIView(APIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]

    def post(self, request, course_id):
        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

        # Retrieve the learner associated with the current user
        learner = Learner.objects.filter(owner=request.user).first()
        if not learner:
            return Response({"error": "Learner profile not found for the current user"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Add the learner's user instance to the course's students
        course.students.add(learner.owner)
        return Response({"message": "Student enrolled successfully"}, status=status.HTTP_200_OK)


class CourseByCategoryList(ListAPIView):
    serializer_class = CourseSerializer

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        if category_id is not None:
            try:
                category = Category.objects.get(pk=category_id)
                return category.course_set.all()  # Assuming you have a reverse relation from Category to Course
            except Category.DoesNotExist:
                return Course.objects.none()
        else:
            return Course.objects.none()


class CourseByInstructorList(ListAPIView):
    serializer_class = CourseSerializer

    def get_queryset(self):
        instructor_id = self.kwargs.get('instructor_id')
        # this will return the user id  not the teacher profile id
        # teacher__id = instructor_id
        if instructor_id is not None:
            try:
                instructor = Instructor.objects.get(id=instructor_id)
                user = instructor.owner
                return Course.objects.filter(teacher=user)
            except Instructor.DoesNotExist:
                return Course.objects.none()
        else:
            return Course.objects.none()  # Return empty queryset if no instructor_id is provided


class TagsByCourseList(ListAPIView):
    serializer_class = TagsSerializer

    def get_queryset(self):
        course_id = self.kwargs.get('course_id')
        if course_id is not None:
            try:
                course = Course.objects.get(id=course_id)
                return course.tags.all()
            except Course.DoesNotExist:
                return Tags.objects.none()
        else:
            return Tags.objects.none()
