from rest_framework import generics, permissions

from wissen_api.permissions import IsOwnerOrReadOnly
from .models import Rating
from .serializer import RatingSerializer


class RatingList(generics.ListCreateAPIView):
    """
    List Ratings or create a rate if logged in.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = RatingSerializer
    queryset = Rating.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RatingDetail(generics.RetrieveDestroyAPIView):
    """
    Retrieve a like or delete it by id if you own it.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = RatingSerializer
    queryset = Rating.objects.all()
