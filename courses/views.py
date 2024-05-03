from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from wissen_api.permissions import HasInstructorProfile
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
