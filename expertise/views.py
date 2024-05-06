from rest_framework import generics, permissions

from instructor.models import Instructor
from instructor.serializers import InstructorSerializer
from .models import Expertise
from .serializers import ExpertiseSerializer


class ExpertiseList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ExpertiseSerializer
    queryset = Expertise.objects.all()


class ExpertiseDetail(generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ExpertiseSerializer
    queryset = Expertise.objects.all()


class InstructorsByExpertiseList(generics.ListAPIView):
    serializer_class = InstructorSerializer

    def get_queryset(self):
        expertise_id = self.kwargs.get('pk')
        if expertise_id is not None:
            try:
                tag = Expertise.objects.get(id=expertise_id)
                return tag.courses.all()
            except Expertise.DoesNotExist:
                return Instructor.objects.none()
        else:
            return Instructor.objects.none()
