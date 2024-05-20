from rest_framework import generics, permissions

from wissen_api.permissions import IsOwnerOrReadOnly
from .models import Learner
from .serializers import LearnerSerializer


class LearnerList(generics.ListCreateAPIView):
    """
    List comments or create a comment if logged in.
    """

    serializer_class = LearnerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Learner.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LearnerDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a comment, or update or delete it by id if you own it.
    """

    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = LearnerSerializer
    queryset = Learner.objects.all()
