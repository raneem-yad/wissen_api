from rest_framework import permissions

from instructor.models import Instructor


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsInstructorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.teacher == request.user


class HasInstructorProfile(permissions.BasePermission):
    """
    to give permission only for an instructor to create a course
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False

        # Check if the user has an instructor profile
        try:
            instructor = Instructor.objects.get(owner=request.user)
            return True
        except Instructor.DoesNotExist:
            return False

