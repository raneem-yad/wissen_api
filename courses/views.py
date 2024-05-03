from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Course
from .serializers import CourseSerializer


class CourseList(APIView):
    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(
            courses, many=True, context={'request': request}
        )
        return Response(serializer.data)
