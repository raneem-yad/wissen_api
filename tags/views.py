from rest_framework import generics, permissions

from courses.models import Course
from courses.serializers import CourseSerializer
from .models import Tags
from .serializers import TagsSerializer


class TagsList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TagsSerializer
    queryset = Tags.objects.all()


class TagsDetail(generics.RetrieveDestroyAPIView):
    """
    Retrieve a like or delete it by id if you own it.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TagsSerializer
    queryset = Tags.objects.all()


class CoursesByTagList(generics.ListAPIView):
    serializer_class = CourseSerializer

    def get_queryset(self):
        tag_id = self.kwargs.get('pk')
        if tag_id is not None:
            try:
                tag = Tags.objects.get(id=tag_id)
                return tag.courses.all()
            except Tags.DoesNotExist:
                return Course.objects.none()
        else:
            return Course.objects.none()
