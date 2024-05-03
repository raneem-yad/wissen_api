from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Instructor
from .serializers import InstructorSerializer


class InstructorList(APIView):
    def get(self, request):
        instructors = Instructor.objects.all()
        serializer = InstructorSerializer(instructors, many=True,context={'request': request})
        return Response(serializer.data)