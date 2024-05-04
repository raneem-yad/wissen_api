from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

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