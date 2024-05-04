from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Instructor
from .serializers import InstructorSerializer
from wissen_api.permissions import IsOwnerOrReadOnly


class InstructorList(APIView):
    def get(self, request):
        instructors = Instructor.objects.all()
        serializer = InstructorSerializer(instructors, many=True, context={'request': request})
        return Response(serializer.data)


class InstructorDetails(APIView):
    serializer_class = InstructorSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self, pk):
        try:
            instructor = Instructor.objects.get(pk=pk)
            self.check_object_permissions(self.request, instructor)
            return instructor
        except Instructor.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        instructor = self.get_object(pk)

        serializer = InstructorSerializer(instructor, context={'request': request})
        return Response(serializer.data)

    @swagger_auto_schema(request_body=InstructorSerializer)
    def put(self, request, pk):
        instructor = self.get_object(pk)
        serializer = InstructorSerializer(instructor, data=request.data,  context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


