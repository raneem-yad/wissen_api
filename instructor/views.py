from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Instructor
from .serializers import InstructorSerializer


class InstructorList(APIView):
    def get(self, request):
        instructors = Instructor.objects.all()
        serializer = InstructorSerializer(instructors, many=True, context={'request': request})
        return Response(serializer.data)


class InstructorDetails(APIView):
    def get_object(self, pk):
        try:
            instructor = Instructor.objects.get(pk=pk)
            return instructor
        except Instructor.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        instructor = self.get_object(pk)
        serializer = InstructorSerializer(instructor, context={'request': request})
        return Response(serializer.data)