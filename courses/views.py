from django.contrib.auth.models import User
from django.db.models import Avg
from django.http import Http404, QueryDict
from django.utils.datastructures import MultiValueDict
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404

from category.models import Category
from instructor.models import Instructor
from learner.models import Learner
from rating.models import Rating
from tags.models import Tags
from tags.serializers import TagsSerializer
from wissen_api.permissions import HasInstructorProfile, IsInstructorOrReadOnly
from .models import Course, VideoContent
from .serializers import CourseSerializer, VideoContentSerializer


class CourseList(ListAPIView, CreateAPIView):
    """
        API endpoint to retrieve all courses.
        """
    serializer_class = CourseSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    search_fields = [
        'teacher__username',
        'course_name',
    ]
    ordering_fields = [
        'course_name',
        'comments_count',
        'posted_date',
    ]
    queryset = Course.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        # ?sort_by=name&ascending=true
        # ?sort_by=created_at&ascending=false
        sort_by = self.request.query_params.get('sort_by')
        ascending = self.request.query_params.get('ascending', 'true').lower() == 'true'

        # Define the default ordering
        ordering = '-posted_date'  # Default to descending order of date created

        if sort_by == 'name':
            ordering = 'course_name' if ascending else '-course_name'

        if sort_by == 'posted_date':
            ordering = 'posted_date' if ascending else '-posted_date'

        return queryset.order_by(ordering)

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)

    @swagger_auto_schema(request_body=CourseSerializer)
    def post(self, request, *args, **kwargs):
        # Allow only instructors to create a course
        if not HasInstructorProfile().has_permission(request, self):
            return Response(
                {"detail": "You must have an instructor profile to create a course.",
                 "request": request.user},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().post(request, *args, **kwargs)


class CourseDetails(RetrieveUpdateDestroyAPIView):
    """
        API endpoint to retrieve all details for a specific course.
        """
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]

    def get_queryset(self):
        return Course.objects.all()

    def get_object(self):
        pk = self.kwargs.get('pk')
        try:
            return self.get_queryset().get(pk=pk)
        except Course.DoesNotExist:
            raise Http404

    @swagger_auto_schema(request_body=CourseSerializer)
    def put(self, request, *args, **kwargs):
        # Allow only instructors to update a course
        if not HasInstructorProfile().has_permission(request, self):
            return Response(
                {"detail": "You must have an instructor profile to create a course."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        # Allow only instructors to delete a course
        if not HasInstructorProfile().has_permission(request, self):
            return Response(
                {"detail": "You must have an instructor profile to create a course."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().delete(request, *args, **kwargs)


class EnrollStudentAPIView(APIView):
    """
        API endpoint to enroll in course.
        """
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]

    def post(self, request, course_id):
        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

        # Retrieve the learner associated with the current user
        learner = Learner.objects.filter(owner=request.user).first()
        if not learner:
            return Response({"error": "Learner profile not found for the current user"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Add the learner's user instance to the course's students
        course.students.add(learner.owner)
        return Response({"message": "Student enrolled successfully"}, status=status.HTTP_200_OK)


class CourseByCategoryList(ListAPIView):
    """
        API endpoint to retrieve all courses for a specific category.
        """
    serializer_class = CourseSerializer

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        if category_id is not None:
            try:
                category = Category.objects.get(pk=category_id)
                return category.course_set.all()  # Assuming you have a reverse relation from Category to Course
            except Category.DoesNotExist:
                return Course.objects.none()
        else:
            return Course.objects.none()


class CourseByInstructorList(ListAPIView):
    """
        API endpoint to retrieve all courses for a specific instructor.
        """
    serializer_class = CourseSerializer

    def get_queryset(self):
        instructor_id = self.kwargs.get('instructor_id')
        # this will return the user id  not the teacher profile id
        # teacher__id = instructor_id
        if instructor_id is not None:
            try:
                instructor = Instructor.objects.get(id=instructor_id)
                user = instructor.owner
                return Course.objects.filter(teacher=user)
            except Instructor.DoesNotExist:
                return Course.objects.none()
        else:
            return Course.objects.none()  # Return empty queryset if no instructor_id is provided


class TagsByCourseList(ListAPIView):
    """
        API endpoint to retrieve all tags for a specific course.
        """
    serializer_class = TagsSerializer

    def get_queryset(self):
        course_id = self.kwargs.get('course_id')
        if course_id is not None:
            try:
                course = Course.objects.get(id=course_id)
                return course.tags.all()
            except Course.DoesNotExist:
                return Tags.objects.none()
        else:
            return Tags.objects.none()


class CourseVideoListView(APIView):
    """
    API endpoint to retrieve all videos for a specific course.
    """

    def get(self, request, course_id):
        course = get_object_or_404(Course, pk=course_id)
        videos = VideoContent.objects.filter(video_contents=course)
        serializer = VideoContentSerializer(videos, many=True)
        return Response(serializer.data)

    def post(self, request, course_id):
        serializer = VideoContentSerializer(data=request.data)
        if serializer.is_valid():
            course = get_object_or_404(Course, pk=course_id)
            serializer.validated_data['course'] = course
            video_content = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseVideoDetailView(APIView):
    def put(self, request, course_id, video_id):
        video_content = get_object_or_404(VideoContent, pk=video_id)
        serializer = VideoContentSerializer(video_content, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, course_id, video_id):
        video_content = get_object_or_404(VideoContent, pk=video_id)
        video_content.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TopThreeCoursesView(APIView):
    def get(self, request):
        # Query the Rating model to get the top-rated courses
        top_rated_course_ids = Rating.objects.values('course').annotate(avg_rating=Avg('rating')).order_by(
            '-avg_rating')[:3].values_list('course', flat=True)

        # Retrieve the top-rated courses
        top_rated_courses = Course.objects.filter(id__in=top_rated_course_ids)

        # Serialize the data using CourseSerializer
        serialized_courses = CourseSerializer(top_rated_courses, many=True, context={'request': request}).data

        # Return a JsonResponse with the serialized data
        return Response(serialized_courses)
