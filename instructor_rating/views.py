from rest_framework import generics, permissions

from wissen_api.permissions import IsOwnerOrReadOnly
from .models import InstructorRating
from .serializers import InstructorRatingSerializer


class InstructorRatingList(generics.ListCreateAPIView):
    """
    List Ratings or create a rate if logged in.
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = InstructorRatingSerializer
    queryset = InstructorRating.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class InstructorRatingDetail(generics.RetrieveDestroyAPIView):
    """
    Retrieve a like or delete it by id if you own it.
    """

    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = InstructorRatingSerializer
    queryset = InstructorRating.objects.all()
