from rest_framework import permissions

from instructor.models import Instructor


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print("yeah will print")
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class HasInstructorProfile(permissions.BasePermission):
    """
    to give permission only for an instructor to create a course
    """

    # def has_permission(self, request, view):
    #     return hasattr(request.user, 'instructor')
    #
    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False
        # Check if the user has an instructor profile
        try:
            instructor = Instructor.objects.get(owner=request.user)
            print("Instructor found:", instructor)
            return True
        except Instructor.DoesNotExist:
            print("Instructor not found for user:", request.user)
            return False

