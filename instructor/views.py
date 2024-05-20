from django.db.models import Avg
from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from expertise.models import Expertise
from expertise.serializers import ExpertiseSerializer
from .models import Instructor
from .serializers import InstructorSerializer
from wissen_api.permissions import IsOwnerOrReadOnly


class InstructorList(APIView):
    def get(self, request):
        instructors = Instructor.objects.all()
        serializer = InstructorSerializer(
            instructors, many=True, context={"request": request}
        )
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

        serializer = InstructorSerializer(
            instructor, context={"request": request}
        )
        return Response(serializer.data)

    @swagger_auto_schema(request_body=InstructorSerializer)
    def put(self, request, pk):
        instructor = self.get_object(pk)
        serializer = InstructorSerializer(
            instructor, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExpertiseByInstructorList(generics.ListAPIView):
    serializer_class = ExpertiseSerializer

    def get_queryset(self):
        instructor_id = self.kwargs.get("pk")
        if instructor_id is not None:
            try:
                course = Instructor.objects.get(id=instructor_id)
                return course.tags.all()
            except Instructor.DoesNotExist:
                return Expertise.objects.none()
        else:
            return Expertise.objects.none()


class TopInstructorsView(APIView):
    def get(self, request):
        # Get the top 6 instructors based on average rating
        top_instructors = Instructor.objects.annotate(
            avg_rating=Avg("instructor_ratings__rating")
        ).order_by("-avg_rating")[:6]

        # Serialize the queryset
        serializer = InstructorSerializer(
            top_instructors, many=True, context={"request": request}
        )

        return Response(serializer.data)
