from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from wissen_api.permissions import HasInstructorProfile
from .models import Category
from .serializers import CategorySerializer


class CategoryList(APIView):
    serializer_class = CategorySerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(
            categories, many=True, context={'request': request}
        )
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CategorySerializer)
    def post(self, request):
        # Allow only instructors to create a course
        if not HasInstructorProfile().has_permission(request, self):
            return Response(
                {"detail": "You must have an instructor profile to create a Category."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = CategorySerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class CategoryDetails(APIView):
    serializer_class = CategorySerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]

    def get_object(self, pk):
        try:
            category = Category.objects.get(pk=pk)
            self.check_object_permissions(self.request, category)
            return category
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        category = self.get_object(pk)

        serializer = CategorySerializer(category, context={'request': request})
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CategorySerializer)
    def put(self, request, pk):
        # Allow only instructors to create a course
        if not HasInstructorProfile().has_permission(request, self):
            return Response(
                {"detail": "You must have an instructor profile to create a Category."},
                status=status.HTTP_403_FORBIDDEN
            )

        category = self.get_object(pk)
        serializer = CategorySerializer(category, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # Allow only instructors to create a course
        if not HasInstructorProfile().has_permission(request, self):
            return Response(
                {"detail": "You must have an instructor profile to create a Category."},
                status=status.HTTP_403_FORBIDDEN
            )

        category = self.get_object(pk)
        category.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
